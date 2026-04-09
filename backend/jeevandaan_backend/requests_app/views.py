from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from .models import AttenderRequest, PartnerDonorRequest
from .serializers import (
    AttenderRequestSerializer,
    AttenderRequestPublicSerializer,
    PartnerDonorRequestSerializer,
    PartnerDonorRequestPublicSerializer
)
from users.models import Donor
from partners.models import Partners
import jwt
import os
from notifications.helpers import notify_nearby_donors
from users.location import get_nearby_partners, get_nearby_donors
from .models import AttenderRating, DonorRating


# ── helper — decode token ────────────────────────────
def decode_token(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])


# ════════════════════════════════════════════════════
#  ATTENDER REQUESTS
# ════════════════════════════════════════════════════

class AttenderRequestCreateView(APIView):

    def post(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only registered users can raise requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])

            # Check one request rule for unverified donors
            if not donor.is_aadhaar_verified:
                if donor.total_requests_raised >= 1:
                    return Response(
                        {'error': 'Verify Aadhaar to raise more requests.'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer = AttenderRequestSerializer(data=request.data)
            if serializer.is_valid():
                # Auto set expiry — 20 hours from now
                expires_at = timezone.now() + timedelta(hours=20)
                req = serializer.save(
                    attender=donor,
                    expires_at=expires_at
                )

                # Increment request count
                donor.total_requests_raised += 1
                donor.save()

                return Response({
                    'message': 'Request raised successfully.',
                    'reference_id': str(req.reference_id),
                    'request': AttenderRequestSerializer(req).data
                }, status=status.HTTP_201_CREATED)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Donor.DoesNotExist:
            return Response({'error': 'Donor not found.'}, status=status.HTTP_404_NOT_FOUND)


class AttenderRequestListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Public — all pending requests visible to partners
        requests = AttenderRequest.objects.filter(
            status='pending'
        ).order_by('-created_at')

        urgency = request.query_params.get('urgency')
        blood_group = request.query_params.get('blood_group')

        if urgency:
            requests = requests.filter(urgency=urgency)
        if blood_group:
            requests = requests.filter(blood_group=blood_group)

        return Response(
            AttenderRequestPublicSerializer(requests, many=True).data
        )


class AttenderRequestDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, reference_id):
        try:
            req = AttenderRequest.objects.get(reference_id=reference_id)
            return Response(AttenderRequestSerializer(req).data)
        except AttenderRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


# ════════════════════════════════════════════════════
#  PARTNER DONOR REQUESTS
# ════════════════════════════════════════════════════

class PartnerDonorRequestCreateView(APIView):

    def post(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can raise donor requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner = Partners.objects.get(id=payload['id'])
            serializer = PartnerDonorRequestSerializer(data=request.data)

            if serializer.is_valid():
                expires_at = timezone.now() + timedelta(hours=12)
                req = serializer.save(
                    partner=partner,
                    expires_at=expires_at
                )

                # Auto notify nearby donors!  
                notify_nearby_donors(
                    blood_group=req.blood_group,
                    partner_lat=partner.latitude,
                    partner_lng=partner.longitude,
                    message=f'Urgent! {req.blood_group} blood needed at {partner.hospital_name}. Please donate!',
                    radius_km=10
                )

                return Response({
                    'message': 'Donor request raised successfully.',
                    'request': PartnerDonorRequestSerializer(req).data
                }, status=status.HTTP_201_CREATED)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)



class PartnerDonorRequestListView(APIView):
    permission_classes = [AllowAny]

    DEFAULT_RADIUS_KM = 10      
    FALLBACK_RADIUS_KM = 50    

    def get(self, request):
        donor_lat   = request.query_params.get('lat')
        donor_lon   = request.query_params.get('lon')
        blood_group = request.query_params.get('blood_group')

        print("=== REQUEST HIT ===")
        print("donor_lat:", donor_lat)
        print("donor_lon:", donor_lon)
        print("blood_group:", blood_group)

        open_requests = PartnerDonorRequest.objects.filter(
    status='open'  # ← include assigned
).select_related('partner').order_by('-created_at')

        if blood_group:
            open_requests = open_requests.filter(blood_group=blood_group)
            print("AFTER BG FILTER:", open_requests.count())
        print("lat/lon present?", bool(donor_lat and donor_lon))

        if donor_lat and donor_lon:
            partners_in_requests = list(set([req.partner for req in open_requests]))
            print("UNIQUE PARTNERS:", len(partners_in_requests))

            for p in partners_in_requests:

                print(f"Partner: {p.hospital_name} | lat: {p.latitude} | lng: {p.longitude}")


            nearby_partners = get_nearby_partners(
                donor_lat, donor_lon,
                partners_in_requests,
                radius_km=self.DEFAULT_RADIUS_KM  
            )

            distance_map = {
                item['partner'].id: item['distance_km']
                for item in nearby_partners
            }
            nearby_partner_ids = list(distance_map.keys())

            open_requests = open_requests.filter(partner_id__in=nearby_partner_ids)

            data = PartnerDonorRequestPublicSerializer(open_requests, many=True).data
            for item in data:
                partner_id = next(
                    (req.partner_id for req in open_requests if req.id == item['id']),
                    None
                )
                item['distance_km'] = distance_map.get(partner_id, None)

            data = sorted(data, key=lambda x: x['distance_km'] or 999)
            return Response(data)

        
        return Response(
            PartnerDonorRequestPublicSerializer(open_requests, many=True).data
        )
    
class PartnerDonorRequestListDetailView(APIView):
    permission_classes = [AllowAny]

    DEFAULT_RADIUS_KM = 10      
    FALLBACK_RADIUS_KM = 50    

    def get(self, request):
        donor_lat   = request.query_params.get('lat')
        donor_lon   = request.query_params.get('lon')
        blood_group = request.query_params.get('blood_group')

        print("=== REQUEST HIT ===")
        print("donor_lat:", donor_lat)
        print("donor_lon:", donor_lon)
        print("blood_group:", blood_group)

        open_requests = PartnerDonorRequest.objects.filter(
        status__in=['open', 'assigned']  # ← include assigned
).select_related('partner').order_by('-created_at')

        if blood_group:
            open_requests = open_requests.filter(blood_group=blood_group)
            print("AFTER BG FILTER:", open_requests.count())
        print("lat/lon present?", bool(donor_lat and donor_lon))

        if donor_lat and donor_lon:
            partners_in_requests = list(set([req.partner for req in open_requests]))
            print("UNIQUE PARTNERS:", len(partners_in_requests))

            for p in partners_in_requests:

                print(f"Partner: {p.hospital_name} | lat: {p.latitude} | lng: {p.longitude}")


            nearby_partners = get_nearby_partners(
                donor_lat, donor_lon,
                partners_in_requests,
                radius_km=self.DEFAULT_RADIUS_KM  
            )

            distance_map = {
                item['partner'].id: item['distance_km']
                for item in nearby_partners
            }
            nearby_partner_ids = list(distance_map.keys())

            open_requests = open_requests.filter(partner_id__in=nearby_partner_ids)

            data = PartnerDonorRequestPublicSerializer(open_requests, many=True).data
            for item in data:
                partner_id = next(
                    (req.partner_id for req in open_requests if req.id == item['id']),
                    None
                )
                item['distance_km'] = distance_map.get(partner_id, None)

            data = sorted(data, key=lambda x: x['distance_km'] or 999)
            return Response(data)

        
        return Response(
            PartnerDonorRequestPublicSerializer(open_requests, many=True).data
        )

class DonorRequestDetailView(APIView):
    """Get single donor request by ID — for chat page"""
    permission_classes = [AllowAny]

    def get(self, request, request_id):
        try:
            token = request.headers.get(
                'Authorization', ''
            ).replace('Bearer ', '').strip()
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )

            req = PartnerDonorRequest.objects.select_related(
                'partner', 'assigned_donor'
            ).get(id=request_id)

            return Response({
                'id': req.id,
                'hospital_name': req.partner.hospital_name,
                'city': req.partner.city,
                'blood_group': req.blood_group,
                'quantity': req.quantity,
                'status': req.status,
                'expires_at': req.expires_at,
                'created_at': req.created_at,
            })

        except PartnerDonorRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found.'},
                status=404
            )
        except Exception as e:
            return Response({'error': str(e)}, status=500)


from .models import OTPCode

class DonorAcceptRequestView(APIView):

    def post(self, request, request_id):
        try:
            payload = decode_token(request)
            donor = Donor.objects.get(id=payload['id'])

            if donor.is_locked:
                return Response(
                    {'error': 'Your account is locked.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            req = PartnerDonorRequest.objects.get(
                id=request_id,
                status='open'
            )

            req.assigned_donor = donor
            req.status = 'assigned'
            req.save()

            # Generate OTP
            OTPCode.objects.filter(request=req).delete()
            otp = OTPCode.objects.create(
                request=req,
                code=OTPCode.generate_code()
            )

            #   Create notification for partner
            from notifications.models import Notification
            Notification.objects.create(
                partner=req.partner,
                notification_type='sms',
                trigger='donor_accepted',
                message=f'Donor #{donor.id} has accepted your blood request for {req.blood_group} ({req.quantity} units). OTP: {otp.code}',
                status='pending'
            )

            return Response({
                'message': 'Request accepted!',
                'otp_code': otp.code,
                'request': PartnerDonorRequestSerializer(req).data
            })

        except PartnerDonorRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found or already assigned.'},
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


class DonorCancelRequestView(APIView):

    def post(self, request, request_id):
        try:
            payload = decode_token(request)
            donor = Donor.objects.get(id=payload['id'])

            req = PartnerDonorRequest.objects.get(
                id=request_id,
                assigned_donor=donor,
                status='assigned'
            )

            reason = request.data.get('reason')
            if not reason:
                return Response(
                    {'error': 'Cancellation reason is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Cancel request
            req.status = 'open'
            req.assigned_donor = None
            req.cancellation_reason = reason
            req.save()

            # Deduct score
            donor.reliability_score = max(0, donor.reliability_score - 10)
            donor.cancellation_count += 1

            # Lock account after 3 cancellations
            if donor.cancellation_count >= 3:
                donor.is_locked = True
                donor.locked_until = timezone.now() + timedelta(days=30)

            donor.save()

            return Response({
                'message': 'Request cancelled.',
                'reliability_score': donor.reliability_score
            })

        except PartnerDonorRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

class FulfillAttenderRequestView(APIView):

    def post(self, request, reference_id):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can fulfill requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner = Partners.objects.get(id=payload['id'])

            req = AttenderRequest.objects.get(
                reference_id=reference_id,
                status='pending'
            )

            req.status = 'fulfilled'
            req.save()

            return Response({
                'message': 'Request fulfilled successfully!  ',
                'reference_id': str(req.reference_id)
            })

        except AttenderRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found or already fulfilled.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


class GetRequestOTPView(APIView):

    def get(self, request, request_id):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can view OTP.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            from .models import OTPCode
            otp = OTPCode.objects.get(
                request_id=request_id,
                is_used=False
            )
            return Response({'otp_code': otp.code})

        except OTPCode.DoesNotExist:
            return Response(
                {'otp_code': None},
                status=status.HTTP_200_OK
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

class VerifyOTPView(APIView):
    """Partner verifies donor OTP at bank"""

    def post(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can verify OTP.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            otp_code = request.data.get('otp_code')
            if not otp_code:
                return Response(
                    {'error': 'OTP code is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                otp = OTPCode.objects.get(code=otp_code, is_used=False)
            except OTPCode.DoesNotExist:
                return Response(
                    {'error': 'Invalid or already used OTP.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Mark OTP as used
            from django.utils import timezone
            otp.is_used = True
            otp.used_at = timezone.now()
            otp.save()

            return Response({
                'message': 'OTP verified successfully!  ',
                'request_id': otp.request.id,
                'blood_group': otp.request.blood_group,
                'quantity': otp.request.quantity,
            })

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)




class DonorPartnerRequestListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()

            if not token:
                return Response({'error': 'No token provided.'}, status=401)

            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            # Must be partner
            if payload.get('type') != 'partner':
                return Response({'error': 'Only partners can access this.'}, status=403)

            partner = Partners.objects.get(id=payload['id'])

            # Fetch only THIS partner's requests
            requests = PartnerDonorRequest.objects.filter(
                partner=partner,
                status__in=['open', 'assigned']
            ).select_related('partner', 'assigned_donor').order_by('-created_at')

            data = PartnerDonorRequestPublicSerializer(requests, many=True).data
            return Response(data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=401)
        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# rating

class SubmitAttenderRatingView(APIView):
    """Attender rates partner after request fulfilled"""

    def post(self, request, reference_id):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only attenders can rate.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])
            req = AttenderRequest.objects.get(
                reference_id=reference_id,
                attender=donor,
                status='fulfilled'
            )

            # Check not already rated
            if AttenderRating.objects.filter(request=req).exists():
                return Response(
                    {'error': 'Already rated this request.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stars = request.data.get('stars')
            review = request.data.get('review', '')
            has_complaint = request.data.get('has_complaint', False)
            complaint_type = request.data.get('complaint_type', None)
            complaint_detail = request.data.get('complaint_detail', '')

            if not stars or int(stars) not in range(1, 6):
                return Response(
                    {'error': 'Stars must be between 1 and 5.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            rating = AttenderRating.objects.create(
                attender=donor,
                partner=req.partner if hasattr(req, 'partner') else None,
                request=req,
                stars=int(stars),
                review=review,
                has_complaint=has_complaint,
                complaint_type=complaint_type if has_complaint else None,
                complaint_detail=complaint_detail if has_complaint else ''
            )

            # Check bad ratings — suspend if 5+
            if has_complaint:
                bad_count = AttenderRating.objects.filter(
                    partner=rating.partner,
                    has_complaint=True
                ).count()

                if bad_count >= 5:
                    rating.partner.is_live = False
                    rating.partner.save()

            return Response({
                'message': 'Rating submitted successfully!  ',
                'stars': stars
            }, status=status.HTTP_201_CREATED)

        except AttenderRequest.DoesNotExist:
            return Response(
                {'error': 'Fulfilled request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


class SubmitDonorRatingView(APIView):
    """Donor rates partner after donation fulfilled"""

    def post(self, request, request_id):
        try:
            payload = decode_token(request)

            # Only DONOR can rate  
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only donors can submit ratings.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])

            # Find the request assigned to THIS donor
            req = PartnerDonorRequest.objects.get(
                id=request_id,
                assigned_donor=donor,      # ← must be assigned to this donor
                status='fulfilled'         # ← only after fulfilled
            )

            # Check not already rated
            if DonorRating.objects.filter(request=req).exists():
                return Response(
                    {'error': 'You have already rated this request.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stars = int(request.data.get('stars', 5))
            review = request.data.get('review', '')

            if stars not in range(1, 6):
                return Response(
                    {'error': 'Stars must be between 1 and 5.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Donor rates the PARTNER
            DonorRating.objects.create(
                partner=req.partner,       # ← partner being rated
                donor=donor,               # ← donor who is rating
                request=req,
                stars=stars,
                review=review
            )

            # Update partner reliability based on rating
            partner = req.partner
            if stars >= 4:
                # Good rating → partner score up
                partner.convenience_fee = partner.convenience_fee  # no change
            elif stars <= 2:
                # Bad rating → check complaints
                bad_ratings = DonorRating.objects.filter(
                    partner=partner,
                    stars__lte=2
                ).count()

                if bad_ratings >= 5:
                    partner.is_live = False  # ← suspend after 5 bad ratings
                    partner.save()

            return Response({
                'message': 'Rating submitted successfully! Thank you 🙏'
            }, status=status.HTTP_201_CREATED)

        except PartnerDonorRequest.DoesNotExist:
            return Response(
                {'error': 'Fulfilled request not found or not assigned to you.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Donor.DoesNotExist:
            return Response(
                {'error': 'Donor not found.'},
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

class MyAttenderRequestsView(APIView):
    """Donor sees their own raised requests"""

    def get(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only donors can access this.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])

            requests = AttenderRequest.objects.filter(
                attender=donor
            ).order_by('-created_at')

            data = []
            for req in requests:
                # Check if already rated
                is_rated = AttenderRating.objects.filter(
                    request=req
                ).exists()

                data.append({
                    'reference_id': str(req.reference_id),
                    'patient_name': req.patient_name,
                    'blood_group': req.blood_group,
                    'quantity': req.quantity,
                    'urgency': req.urgency,
                    'hospital_name': req.hospital_name,
                    'city': req.city,
                    'status': req.status,
                    'is_rated': is_rated,
                    'expires_at': req.expires_at,
                    'created_at': req.created_at,
                    'updated_at': req.updated_at,
                })

            return Response(data)

        except Donor.DoesNotExist:
            return Response(
                {'error': 'Donor not found.'},
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