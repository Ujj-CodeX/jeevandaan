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

                # Auto notify nearby donors! ✅
                notify_nearby_donors(
                    blood_group=req.blood_group,
                    city=partner.city,
                    message=f'Urgent! {req.blood_group} blood needed at {partner.hospital_name}. Please donate!'
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

    def get(self, request):
        # Open requests visible to all nearby donors
        requests = PartnerDonorRequest.objects.filter(
            status='open'
        ).order_by('-created_at')

        blood_group = request.query_params.get('blood_group')
        city = request.query_params.get('city')

        if blood_group:
            requests = requests.filter(blood_group=blood_group)
        if city:
            requests = requests.filter(partner__city__icontains=city)

        return Response(
            PartnerDonorRequestPublicSerializer(requests, many=True).data
        )


class DonorAcceptRequestView(APIView):

    def post(self, request, request_id):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only donors can accept requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])

            # Check if donor account is locked
            if donor.is_locked:
                return Response(
                    {'error': 'Your account is locked.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            req = PartnerDonorRequest.objects.get(id=request_id, status='open')
            req.assigned_donor = donor
            req.status = 'assigned'
            req.save()

            return Response({
                'message': 'Request accepted successfully.',
                'request': PartnerDonorRequestSerializer(req).data
            })

        except PartnerDonorRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found or already assigned.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


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