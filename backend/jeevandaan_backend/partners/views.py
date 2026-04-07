from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
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
                stocks = Stock.objects.filter(partner=item['partner'])
                stock_dict = {s.blood_group: s.quantity for s in stocks}

                # Always assign it, even if empty {}
                partner_data['available_units'] = stock_dict if stock_dict else None
                

            result.append(partner_data)

        return Response(result)


class NearbyDonorsView(APIView):

    def get(self, request):
        try:
            

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        

        try:
            
            partner = request.user
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

            return Response({'message': 'Location updated  '})

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
                    'message': 'Camp created successfully!  ',
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
                'message': f'Camp scheduled! {total_notified} donors notified  ',
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



# ── Fetch Enrolled Camps for a specific Donor ──────────
class EnrolledCampsListView(APIView):
    """
    Returns a list of all camps the currently logged-in donor 
    has enrolled in.
    """
    def get(self, request):
        try:
            # 1. Decode token to get Donor ID
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            # 2. Security Check: Ensure the token belongs to a donor
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Unauthorized. Donor access required.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            donor_id = payload.get('id')

            # 3. Fetch enrollments for this donor
            # We select_related('camp') to optimize the database query
            enrollments = CampEnrollment.objects.filter(donor_id=donor_id).select_related('camp')

            # 4. Serialize the Camp data through the enrollment
            result = []
            for entry in enrollments:
                camp_data = DonationCampSerializer(entry.camp).data
                # Add enrollment-specific info (like date joined)
                camp_data['enrolled_at'] = entry.enrolled_at 
                result.append(camp_data)

            return Response(result, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

            
            camp.stock_updated_after_camp = True
            camp.status = 'completed'
            camp.save()

            return Response({
                'message': 'Stock updated! ',
                'camp': DonationCampSerializer(camp).data
            })

        except DonationCamp.DoesNotExist:
            return Response({'error': 'Camp not found.'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)




import csv
from django.http import HttpResponse

class DownloadCampEnrollmentsView(APIView):

    def get(self, request, camp_id):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can download.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            camp = DonationCamp.objects.get(
                id=camp_id,
                organizer__id=payload['id']
            )

            # Only allow download on camp date or after
            from datetime import date
            if camp.camp_date > date.today():
                return Response(
                    {'error': 'Download available only on or after camp date.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            enrollments = CampEnrollment.objects.filter(camp=camp)

            # Create CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="JeevanDaan_{camp.title}_{camp.camp_date}.csv"'

            writer = csv.writer(response)

            # Header row
            writer.writerow([
                'S.No', 'Name', 'Phone',
                'Blood Group', 'Enrolled At', 'Attended'
            ])

            # Data rows
            for i, enrollment in enumerate(enrollments, 1):
                writer.writerow([
                    i,
                    enrollment.name,
                    enrollment.phone,
                    enrollment.blood_group,
                    enrollment.enrolled_at.strftime('%d %b %Y %I:%M %p'),
                    'Yes' if enrollment.attended else 'No'
                ])

            return response

        except DonationCamp.DoesNotExist:
            return Response(
                {'error': 'Camp not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# Inter Partner Request Handling


class RaiseInterPartnerRequestView(APIView):
    """Bank A requests Bank B for stock"""

    def post(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can raise inter-partner requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            requesting_partner = Partners.objects.get(id=payload['id'])

            blood_group = request.data.get('blood_group')
            quantity = request.data.get('quantity')
            attender_request_id = request.data.get('attender_request_id')

            if not all([blood_group, quantity, attender_request_id]):
                return Response(
                    {'error': 'blood_group, quantity and attender_request_id required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find nearest partner with stock
            from users.location import get_nearby_partners
            from stock.models import Stock
            from requests_app.models import AttenderRequest

            try:
               attender_request = AttenderRequest.objects.get(
               reference_id=attender_request_id,
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

            # Partners with required stock
            partners_with_stock = Partners.objects.filter(
                is_live=True,
                is_verified=True,
                stock__blood_group=blood_group,
                stock__quantity__gte=quantity
            ).exclude(id=requesting_partner.id)

            if not partners_with_stock.exists():
                return Response(
                    {'error': 'No nearby partners have required stock.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Find nearest
            nearby = get_nearby_partners(
                requesting_partner.latitude,
                requesting_partner.longitude,
                partners_with_stock,
                radius_km=20
            )

            if not nearby:
                return Response(
                    {'error': 'No partners found within 20km with required stock.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Pick nearest partner
            fulfilling_partner = nearby[0]['partner']

            from requests_app.models import AttenderRequest, InterPartnerRequest
            attender_req = AttenderRequest.objects.get(
                reference_id=attender_request_id
            )

            inter_req = InterPartnerRequest.objects.create(
                requesting_partner=requesting_partner,
                fulfilling_partner=fulfilling_partner,
                attender_request=attender_req,
                blood_group=blood_group,
                quantity=quantity,
                convenience_fee=fulfilling_partner.convenience_fee
            )

            # Notify fulfilling partner
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
                status='pending'
            )

            return Response({
                'message': f'Request sent to {fulfilling_partner.hospital_name}!  ',
                'fulfilling_partner': PartnerPublicSerializer(fulfilling_partner).data,
                'distance_km': nearby[0]['distance_km'],
                'convenience_fee': str(fulfilling_partner.convenience_fee),
                'inter_request_id': inter_req.id
            }, status=status.HTTP_201_CREATED)

        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


class InterPartnerRequestListView(APIView):
    """Partner sees incoming inter-partner requests"""

    def get(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            partner = Partners.objects.get(id=payload['id'])

            from requests_app.models import InterPartnerRequest
            incoming = InterPartnerRequest.objects.filter(
                fulfilling_partner=partner,
                status='pending'
            ).select_related('requesting_partner', 'attender_request')

            data = []
            for req in incoming:
                data.append({
                    'id': req.id,
                    'requesting_partner': req.requesting_partner.hospital_name,
                    'blood_group': req.blood_group,
                    'quantity': req.quantity,
                    'convenience_fee': str(req.convenience_fee),
                    'status': req.status,
                    'created_at': req.created_at
                })

            return Response(data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


class AcceptInterPartnerRequestView(APIView):
    """Fulfilling partner accepts and marks fulfilled"""

    def post(self, request, inter_request_id):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            partner = Partners.objects.get(id=payload['id'])

            from requests_app.models import InterPartnerRequest
            inter_req = InterPartnerRequest.objects.get(
                id=inter_request_id,
                fulfilling_partner=partner,
                status='pending'
            )

            inter_req.status = 'fulfilled'
            inter_req.save()

            # Update attender request as fulfilled
            inter_req.attender_request.status = 'fulfilled'
            inter_req.attender_request.save()

            # Update stock
            from stock.models import Stock
            stock = Stock.objects.filter(
                partner=partner,
                blood_group=inter_req.blood_group
            ).first()

            if stock:
                stock.quantity = max(0, stock.quantity - inter_req.quantity)
                stock.save()

            return Response({
                'message': 'Inter-partner request fulfilled!  '
            })

        except InterPartnerRequest.DoesNotExist:
            return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
