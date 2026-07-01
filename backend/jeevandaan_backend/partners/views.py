from flask.cli import load_dotenv  # noqa — keep if used elsewhere
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Partners, DonationCamp, CampEnrollment
from .serializers import (
    PartnerRegisterSerializer,
    PartnerLoginSerializer,
    PartnerProfileSerializer,
    PartnerPublicSerializer,
    DonationCampSerializer,
    CampEnrollmentSerializer,
)
import bcrypt
import jwt
import os
import threading
from datetime import datetime, timedelta, date
from users.location import get_nearby_partners, get_nearby_donors
from stock.models import Stock

from config.authentication import PartnerJWTAuthentication
from config.permissions import IsPartner
from config.authentication import DonorJWTAuthentication
from config.permissions import IsDonor
from auth_token.helpers import generate_jwt_token  

from django.core.cache import cache
from users.models import LoginAttempt
from users.utils import get_client_ip

PARTNER_LOGIN_FAIL_LIMIT = 5
PARTNER_LOGIN_FAIL_WINDOW = 15 * 60 


load_dotenv()


# ─────────────────────────────────────────────────────────
def run_in_background(fn, *args, **kwargs):
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start()





# ════════════════════════════════════════════════════════
#  NEARBY
# ════════════════════════════════════════════════════════

class NearbyPartnersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        blood_group = request.query_params.get('blood_group')
        radius = request.query_params.get('radius', 10)

        if not lat or not lng:
            return Response(
                {'error': 'lat and lng are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        partners = Partners.objects.filter(
            is_live=True, is_verified=True,
            latitude__isnull=False, longitude__isnull=False,
        )

        if blood_group:
            partners = partners.filter(
                stock__blood_group=blood_group,
                stock__quantity__gt=0,
            )

        nearby = get_nearby_partners(lat, lng, list(partners), float(radius))

        result = []
        for item in nearby:
            partner_data = PartnerPublicSerializer(item['partner']).data
            partner_data['distance_km'] = item['distance_km']

            if blood_group:
                stocks = Stock.objects.filter(partner=item['partner'])
                stock_dict = {s.blood_group: s.quantity for s in stocks}
                partner_data['available_units'] = stock_dict or None

            result.append(partner_data)

        return Response(result)


class NearbyDonorsView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        blood_group = request.query_params.get('blood_group')
        radius = request.query_params.get('radius', 10)

        if not lat or not lng or not blood_group:
            return Response(
                {'error': 'lat, lng and blood_group are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from users.models import Donor
        donors = Donor.objects.filter(
            blood_group=blood_group,
            is_locked=False,
            is_aadhaar_verified=True,
            latitude__isnull=False,
            longitude__isnull=False,
        )

        nearby = get_nearby_donors(lat, lng, list(donors), float(radius))

        result = [
            {
                'blood_group': item['donor'].blood_group,
                'member_tag': item['donor'].member_tag,
                'reliability_score': item['donor'].reliability_score,
                'distance_km': item['distance_km'],
            }
            for item in nearby
        ]

        return Response(result)


# ════════════════════════════════════════════════════════
#  REGISTER / LOGIN
# ════════════════════════════════════════════════════════

class PartnerRegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PartnerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            partner = serializer.save()
            return Response({
                'message': 'Partner registered successfully.',
                'partner': PartnerProfileSerializer(partner).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.throttling import ScopedRateThrottle
class PartnerLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'  

    def post(self, request):
        serializer = PartnerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        license_id = serializer.validated_data['license_id']
        password   = serializer.validated_data['password']

        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')[:255]

        # ── per-license_id lockout check ──
        fail_key = f'login_fail_partner_{license_id}'
        fail_count = cache.get(fail_key, 0)

        if fail_count >= PARTNER_LOGIN_FAIL_LIMIT:
            LoginAttempt.objects.create(
                identifier=license_id, user_type='partner',
                ip_address=ip, user_agent=ua,
                success=False, reason='rate_limited'
            )
            return Response(
                {'error': 'Too many failed attempts. Try again after 15 minutes.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        try:
            partner = Partners.objects.get(license_id=license_id)
        except Partners.DoesNotExist:
            cache.set(fail_key, fail_count + 1, timeout=PARTNER_LOGIN_FAIL_WINDOW)
            LoginAttempt.objects.create(
                identifier=license_id, user_type='partner',
                ip_address=ip, user_agent=ua,
                success=False, reason='invalid_license_id'
            )
            return Response(
                {'error': 'Invalid License ID or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not bcrypt.checkpw(password.encode(), partner.password.encode()):
            cache.set(fail_key, fail_count + 1, timeout=PARTNER_LOGIN_FAIL_WINDOW)
            LoginAttempt.objects.create(
                identifier=license_id, user_type='partner',
                ip_address=ip, user_agent=ua,
                success=False, reason='invalid_password'
            )
            return Response(
                {'error': 'Invalid License ID or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not partner.is_live:
            LoginAttempt.objects.create(
                identifier=license_id, user_type='partner',
                ip_address=ip, user_agent=ua,
                success=False, reason='not_verified'
            )
            return Response(
                {'error': 'Account not verified yet. Please wait for admin approval.'},
                status=status.HTTP_403_FORBIDDEN
            )
        cache.delete(fail_key)
        LoginAttempt.objects.create(
            identifier=license_id, user_type='partner',
            ip_address=ip, user_agent=ua,
            success=True
        )

        tokens = generate_jwt_token(partner.id, user_type='partner')
        return Response({
            'message': 'Login successful.',
            'tokens': tokens,
            'partner': PartnerProfileSerializer(partner).data
        })


class PartnerPublicListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city')
        partner_type = request.query_params.get('type')

        partners = Partners.objects.filter(is_live=True, is_verified=True)
        if city:
            partners = partners.filter(city=city)
        if partner_type:
            partners = partners.filter(type=partner_type)

        return Response(PartnerPublicSerializer(partners, many=True).data)


class PartnerProfileView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        partner = request.user
        if not isinstance(partner, Partners):
            return Response(
                {'error': 'Invalid user type.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(PartnerProfileSerializer(partner).data)

    def put(self, request):
        partner = request.user
        allowed_fields = [
            'hospital_name', 'contact', 'address',
            'city', 'state', 'facility',
            'convenience_fee', 'fee_description',
        ]
        for field in allowed_fields:
            if field in request.data:
                setattr(partner, field, request.data[field])
        partner.save()
        return Response(PartnerProfileSerializer(partner).data)


class UpdatePartnerLocationView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        partner = request.user
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')

        if not lat or not lng:
            return Response(
                {'error': 'latitude and longitude required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        partner.latitude = lat
        partner.longitude = lng
        partner.save()
        return Response({'message': 'Location updated'})


# ════════════════════════════════════════════════════════
#  DONATION CAMPS
# ════════════════════════════════════════════════════════

class CreateCampView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        partner = request.user
        serializer = DonationCampSerializer(data=request.data)

        if serializer.is_valid():
            camp = serializer.save(
                organizer=partner,
                latitude=partner.latitude,
                longitude=partner.longitude,
                city=partner.city,
            )
            return Response({
                'message': 'Camp created successfully!',
                'camp': DonationCampSerializer(camp).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleAndNotifyCampView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request, camp_id):
        try:
            partner = request.user
            camp = DonationCamp.objects.get(id=camp_id, organizer__id=partner.id)

            # ── FIX: run heavy notification pipeline in background
            def _notify_camp(camp_id):
                try:
                    from notifications.helpers import notify_camp_donors
                    camp_obj = DonationCamp.objects.get(id=camp_id)
                    notify_camp_donors(camp_obj)
                except Exception as e:
                    print(f"[notify_camp_donors error] {e}")

            run_in_background(_notify_camp, camp.id)

            return Response({
                'message': 'Camp scheduled! Donors are being notified in the background.',
                'camp': DonationCampSerializer(camp).data
            })

        except DonationCamp.DoesNotExist:
            return Response(
                {'error': 'Camp not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class PartnerCampsView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        partner = request.user
        camps = DonationCamp.objects.filter(
            organizer=partner
        ).order_by('-camp_date')
        return Response(DonationCampSerializer(camps, many=True).data)


class NearbyCampsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        camps = DonationCamp.objects.filter(
            camp_date__gte=date.today(),
            status='scheduled',
            # ── FIX: only fetch camps that have coordinates set
            latitude__isnull=False,
            longitude__isnull=False,
        ).order_by('camp_date')

        if lat and lng:
            from geopy.distance import geodesic
            result = []
            for camp in camps:
                distance = geodesic(
                    (float(lat), float(lng)),
                    (float(camp.latitude), float(camp.longitude))
                ).km
                if distance <= 20:
                    data = DonationCampSerializer(camp).data
                    data['distance_km'] = round(distance, 1)
                    result.append(data)
            result.sort(key=lambda x: x['distance_km'])
            return Response(result)

        return Response(DonationCampSerializer(camps, many=True).data)


class EnrollCampView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request, camp_id):
        try:
            donor = request.user
            camp = DonationCamp.objects.get(id=camp_id, status='scheduled')

            if CampEnrollment.objects.filter(camp=camp, donor=donor).exists():
                return Response(
                    {'error': 'Already enrolled in this camp.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if camp.camp_date < date.today():
                return Response(
                    {'error': 'Camp has already passed.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            enrollment = CampEnrollment.objects.create(
                camp=camp,
                donor=donor,
                name=request.data.get('name', donor.name),
                phone=request.data.get('phone', donor.phone_number),
                blood_group=request.data.get('blood_group', donor.blood_group),
            )

            return Response({
                'message': 'Enrolled successfully! See you at the camp',
                'enrollment': CampEnrollmentSerializer(enrollment).data
            }, status=status.HTTP_201_CREATED)

        except DonationCamp.DoesNotExist:
            return Response({'error': 'Camp not found.'}, status=status.HTTP_404_NOT_FOUND)


class EnrolledCampsListView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def get(self, request):
        donor = request.user
        enrollments = CampEnrollment.objects.filter(
            donor=donor
        ).select_related('camp')

        result = []
        for entry in enrollments:
            camp_data = DonationCampSerializer(entry.camp).data
            camp_data['enrolled_at'] = entry.enrolled_at
            result.append(camp_data)

        return Response(result, status=status.HTTP_200_OK)


class UpdateStockAfterCampView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request, camp_id):
        try:
            partner = request.user
            camp = DonationCamp.objects.get(id=camp_id, organizer=partner)

            camp.stock_updated_after_camp = True
            camp.status = 'completed'
            camp.save()

            return Response({
                'message': 'Stock updated!',
                'camp': DonationCampSerializer(camp).data
            })

        except DonationCamp.DoesNotExist:
            return Response({'error': 'Camp not found.'}, status=status.HTTP_404_NOT_FOUND)


import csv
from django.http import HttpResponse

class DownloadCampEnrollmentsView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request, camp_id):
        try:
            partner = request.user
            camp = DonationCamp.objects.get(id=camp_id, organizer__id=partner.id)

            if camp.camp_date > date.today():
                return Response(
                    {'error': 'Download available only on or after camp date.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            enrollments = CampEnrollment.objects.filter(camp=camp)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = (
                f'attachment; filename="JeevanDaan_{camp.title}_{camp.camp_date}.csv"'
            )

            writer = csv.writer(response)
            writer.writerow(['S.No', 'Name', 'Phone', 'Blood Group', 'Enrolled At', 'Attended'])

            for i, enrollment in enumerate(enrollments, 1):
                writer.writerow([
                    i,
                    enrollment.name,
                    enrollment.phone,
                    enrollment.blood_group,
                    enrollment.enrolled_at.strftime('%d %b %Y %I:%M %p'),
                    'Yes' if enrollment.attended else 'No',
                ])

            return response

        except DonationCamp.DoesNotExist:
            return Response({'error': 'Camp not found.'}, status=status.HTTP_404_NOT_FOUND)


# ════════════════════════════════════════════════════════
#  INTER-PARTNER REQUESTS
# ════════════════════════════════════════════════════════

class RaiseInterPartnerRequestView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        try:
            partner = request.user
            requesting_partner = Partners.objects.get(id=partner.id)

            blood_group         = request.data.get('blood_group')
            quantity            = request.data.get('quantity')
            attender_request_id = request.data.get('attender_request_id')

            if not all([blood_group, quantity, attender_request_id]):
                return Response(
                    {'error': 'blood_group, quantity and attender_request_id required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            from requests_app.models import AttenderRequest, InterPartnerRequest

            try:
                attender_request = AttenderRequest.objects.get(
                    reference_id=attender_request_id
                )
            except AttenderRequest.DoesNotExist:
                return Response(
                    {'error': 'Invalid attender_request_id.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if attender_request.status == 'fulfilled':
                return Response(
                    {'error': 'Request already fulfilled.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            partners_with_stock = Partners.objects.filter(
                is_live=True,
                is_verified=True,
                stock__blood_group=blood_group,
                stock__quantity__gte=quantity,
                latitude__isnull=False,
                longitude__isnull=False,
            ).exclude(id=requesting_partner.id)

            if not partners_with_stock.exists():
                return Response(
                    {'error': 'No nearby partners have required stock.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            nearby = get_nearby_partners(
                requesting_partner.latitude,
                requesting_partner.longitude,
                list(partners_with_stock),
                radius_km=20,
            )

            if not nearby:
                return Response(
                    {'error': 'No partners found within 20km with required stock.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            fulfilling_partner = nearby[0]['partner']

            inter_req = InterPartnerRequest.objects.create(
                requesting_partner=requesting_partner,
                fulfilling_partner=fulfilling_partner,
                attender_request=attender_request,
                blood_group=blood_group,
                quantity=quantity,
                convenience_fee=fulfilling_partner.convenience_fee,
            )

            # ── FIX: notification in background
            def _notify():
                from notifications.models import Notification
                Notification.objects.create(
                    partner=fulfilling_partner,
                    notification_type='sms',
                    trigger='donor_request',
                    message=(
                        f"Inter-partner blood request from "
                        f"{requesting_partner.hospital_name}! "
                        f"Need {quantity} units of {blood_group}. "
                        f"Convenience fee: ₹{fulfilling_partner.convenience_fee}"
                    ),
                    status='pending',
                )
            run_in_background(_notify)

            return Response({
                'message': f'Request sent to {fulfilling_partner.hospital_name}!',
                'fulfilling_partner': PartnerPublicSerializer(fulfilling_partner).data,
                'distance_km': nearby[0]['distance_km'],
                'convenience_fee': str(fulfilling_partner.convenience_fee),
                'inter_request_id': inter_req.id,
            }, status=status.HTTP_201_CREATED)

        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)


class InterPartnerRequestListView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        partner = request.user

        from requests_app.models import InterPartnerRequest
        incoming = InterPartnerRequest.objects.filter(
            fulfilling_partner=partner,
            status='pending',
        ).select_related('requesting_partner', 'attender_request')

        data = [
            {
                'id': req.id,
                'requesting_partner': req.requesting_partner.hospital_name,
                'blood_group': req.blood_group,
                'quantity': req.quantity,
                'convenience_fee': str(req.convenience_fee),
                'status': req.status,
                'created_at': req.created_at,
            }
            for req in incoming
        ]

        return Response(data)


class AcceptInterPartnerRequestView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request, inter_request_id):
        try:
            partner = request.user

            from requests_app.models import InterPartnerRequest
            inter_req = InterPartnerRequest.objects.select_related(
                'attender_request'
            ).get(
                id=inter_request_id,
                fulfilling_partner=partner,
                status='pending',
            )

            inter_req.status = 'fulfilled'
            inter_req.save()

            inter_req.attender_request.status = 'fulfilled'
            inter_req.attender_request.save()

            stock = Stock.objects.filter(
                partner=partner,
                blood_group=inter_req.blood_group,
            ).first()

            if stock:
                stock.quantity = max(0, stock.quantity - inter_req.quantity)
                stock.save()

            return Response({'message': 'Inter-partner request fulfilled!'})

        except InterPartnerRequest.DoesNotExist:
            return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)