from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Partners,DonationCamp, CampEnrollment
from .serializers import (
    PartnerRegisterSerializer,
    PartnerLoginSerializer,
    PartnerProfileSerializer,
    PartnerPublicSerializer,
    DonationCampSerializer, CampEnrollmentSerializer
)
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from users.location import get_nearby_partners, get_nearby_donors
from stock.models import Stock
from datetime import date



#--token_generation----------------------
load_dotenv() 


def generate_partner_token(partner_id):
    access_payload = {
        'id': partner_id,
        'type': 'partner',
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),

    }
    refresh_payload = {
        'id': partner_id,
        'type': 'partner',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }
    access = jwt.encode(access_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    refresh = jwt.encode(refresh_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return {'access': access, 'refresh': refresh}



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
            is_live=True,
            is_verified=True
        )

        if blood_group:
            partners = partners.filter(
                stock__blood_group=blood_group,
                stock__quantity__gt=0
            )

        nearby = get_nearby_partners(lat, lng, partners, float(radius))

        result = []
        for item in nearby:
            partner_data = PartnerPublicSerializer(item['partner']).data
            partner_data['distance_km'] = item['distance_km']

            if blood_group:
                stock = Stock.objects.filter(
                    partner=item['partner'],
                    blood_group=blood_group
                ).first()
                partner_data['available_units'] = stock.quantity if stock else 0

            result.append(partner_data)

        return Response(result)


class NearbyDonorsView(APIView):

    def get(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can search donors.'},
                    status=status.HTTP_403_FORBIDDEN
                )

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
                is_aadhaar_verified=True
            )

            nearby = get_nearby_donors(lat, lng, donors, float(radius))

            result = []
            for item in nearby:
                result.append({
                    'blood_group': item['donor'].blood_group,
                    'member_tag': item['donor'].member_tag,
                    'reliability_score': item['donor'].reliability_score,
                    'distance_km': item['distance_km'],
                })

            return Response(result)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

#------Register---------------------------------

class PartnerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer_class = PartnerRegisterSerializer(data=request.data)
        if serializer_class.is_valid():
            partner = serializer_class.save()
            tokens = generate_partner_token(partner.id)
            return Response({
                'message': 'Partner registered successfully.',
                'tokens': tokens,
                'partner': PartnerProfileSerializer(partner).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


#--------Login ---------------------------------

class PartnerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PartnerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        license_id = serializer.validated_data['license_id']   # ← changed
        password = serializer.validated_data['password']

        try:
            partner = Partners.objects.get(license_id=license_id)  # ← get by license_id
        except Partners.DoesNotExist:
            return Response(
                {'error': 'Invalid License ID or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not bcrypt.checkpw(password.encode(), partner.password.encode()):
            return Response(
                {'error': 'Invalid License ID or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not partner.is_live:
            return Response(
                {'error': 'Account not verified yet. Please wait for admin approval.'},
                status=status.HTTP_403_FORBIDDEN
            )

        tokens = generate_partner_token(partner.id)
        return Response({
            'message': 'Login successful.',
            'tokens': tokens,
            'partner': PartnerProfileSerializer(partner).data
        })
    
    
        
class PartnerPublicListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city')
        partner_type = request.query_params.get('type')

        partners = Partners.objects.filter(is_live=True , is_verified=True)
        if city:
            partners = partners.filter(city=city)
        if partner_type:
            partners = partners.filter(type=partner_type)
        serializer = PartnerPublicSerializer(partners, many=True)

        return Response(serializer.data)
    
class PartnerProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        print("AUTH HEADER:", auth_header)

        token = auth_header.replace('Bearer ', '').strip()
        print("TOKEN:", token)
        print("SECRET:", os.getenv('SECRET_KEY'))

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            print("PAYLOAD:", payload)

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Invalid token type.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            partner = Partners.objects.get(id=payload['id'])
            return Response(PartnerProfileSerializer(partner).data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            print("JWT ERROR:", str(e))
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if payload.get('type') != 'partner':
                return Response({'error': 'Invalid token type.'}, status=status.HTTP_401_UNAUTHORIZED)

            partner = Partners.objects.get(id=payload['id'])

            # Only allow updating these fields
            allowed_fields = [
                'hospital_name', 'contact', 'address',
                'city', 'state', 'facility',
                'convenience_fee', 'fee_description'
            ]

            for field in allowed_fields:
                if field in request.data:
                    setattr(partner, field, request.data[field])

            partner.save()
            return Response(PartnerProfileSerializer(partner).data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)
        


class UpdatePartnerLocationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            partner = Partners.objects.get(id=payload['id'])

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

            return Response({'message': 'Location updated ✅'})

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)
        
####################################################################
# 
#   Camps Scheduling and Dashobard Freeze Unfreeze APIs 
#
#
####################################################################


class CreateCampView(APIView):

    def post(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can create camps.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner = Partners.objects.get(id=payload['id'])
            serializer = DonationCampSerializer(data=request.data)

            if serializer.is_valid():
                camp = serializer.save(
                    organizer=partner,
                    latitude=partner.latitude,
                    longitude=partner.longitude,
                    city=partner.city
                )

                return Response({
                    'message': 'Camp created successfully! ✅',
                    'camp': DonationCampSerializer(camp).data
                }, status=status.HTTP_201_CREATED)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ── Schedule & Notify ────────────────────────────────
class ScheduleAndNotifyCampView(APIView):

    def post(self, request, camp_id):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can notify.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Get camp
            camp = DonationCamp.objects.get(
                id=camp_id,
                organizer__id=payload['id']
            )

            # 🔥 Use pipeline
            from notifications.helpers import notify_camp_donors

            total_notified = notify_camp_donors(camp)

            return Response({
                'message': f'Camp scheduled! {total_notified} donors notified ✅',
                'notified_count': total_notified,
                'camp': DonationCampSerializer(camp).data
            })

        except DonationCamp.DoesNotExist:
            return Response(
                {'error': 'Camp not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Token expired.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except jwt.InvalidTokenError:
            return Response(
                {'error': 'Invalid token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

# ── Partner's own camps ──────────────────────────────
class PartnerCampsView(APIView):

    def get(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            partner = Partners.objects.get(id=payload['id'])

            camps = DonationCamp.objects.filter(
                organizer=partner
            ).order_by('-camp_date')

            return Response(DonationCampSerializer(camps, many=True).data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ── Nearby camps — for donors ─────────────────────────
class NearbyCampsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        # Only upcoming camps
        camps = DonationCamp.objects.filter(
            camp_date__gte=date.today(),
            status='scheduled'
        ).order_by('camp_date')

        if lat and lng:
            from users.location import get_nearby_partners
            # Reuse nearby function with camp locations
            result = []
            from geopy.distance import geodesic
            for camp in camps:
                if camp.latitude and camp.longitude:
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


# ── Enroll in camp ────────────────────────────────────
class EnrollCampView(APIView):

    def post(self, request, camp_id):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only donors can enroll.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            from users.models import Donor
            donor = Donor.objects.get(id=payload['id'])
            camp = DonationCamp.objects.get(id=camp_id)

            # Check already enrolled
            if CampEnrollment.objects.filter(camp=camp, donor=donor).exists():
                return Response(
                    {'error': 'Already enrolled in this camp.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check camp date not passed
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
                blood_group=request.data.get('blood_group', donor.blood_group)
            )

            return Response({
                'message': 'Enrolled successfully! See you at the camp 🩸',
                'enrollment': CampEnrollmentSerializer(enrollment).data
            }, status=status.HTTP_201_CREATED)

        except DonationCamp.DoesNotExist:
            return Response({'error': 'Camp not found.'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ── Update stock after camp ───────────────────────────
class UpdateStockAfterCampView(APIView):

    def post(self, request, camp_id):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can update stock.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            camp = DonationCamp.objects.get(
                id=camp_id,
                organizer__id=payload['id']
            )

            # Mark stock updated → unfreeze dashboard
            camp.stock_updated_after_camp = True
            camp.dashboard_frozen = False
            camp.status = 'completed'
            camp.save()

            return Response({
                'message': 'Stock updated! Dashboard unfrozen ✅',
                'camp': DonationCampSerializer(camp).data
            })

        except DonationCamp.DoesNotExist:
            return Response({'error': 'Camp not found.'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ── Check dashboard freeze status ────────────────────
class CheckDashboardFreezeView(APIView):

    def get(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            partner = Partners.objects.get(id=payload['id'])

            # Check if any past camp without stock update
            frozen_camp = DonationCamp.objects.filter(
                organizer=partner,
                camp_date__lt=date.today(),
                stock_updated_after_camp=False,
                status='scheduled'
            ).first()

            if frozen_camp:
                # Auto freeze
                frozen_camp.dashboard_frozen = True
                frozen_camp.save()

                return Response({
                    'is_frozen': True,
                    'frozen_camp': DonationCampSerializer(frozen_camp).data,
                    'message': 'Please update stock from your recent donation camp to unlock dashboard.'
                })

            return Response({'is_frozen': False})

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)