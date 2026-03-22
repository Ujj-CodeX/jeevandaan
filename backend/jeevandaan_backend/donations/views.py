from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import DonationHistory
from .serializers import DonationHistorySerializer
from users.models import Donor
from partners.models import Partners
from requests_app.models import PartnerDonorRequest
import jwt
import os


# ── helper ───────────────────────────────────────────
def decode_token(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])


# ════════════════════════════════════════════════════
#  BANK VERIFIES DONATION
# ════════════════════════════════════════════════════

class VerifyDonationView(APIView):

    def post(self, request, request_id):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can verify donations.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner = Partners.objects.get(id=payload['id'])
            req = PartnerDonorRequest.objects.get(
                id=request_id,
                partner=partner,
                status='assigned'
            )

            donor = req.assigned_donor

            # Create donation history silently
            donation = DonationHistory.objects.create(
                donor=donor,
                partner=partner,
                request=req,
                blood_group=req.blood_group,
                units_donated=req.quantity,
                status='completed',
                score_change=10.0,
                is_verified_by_bank=True,
                verified_at=timezone.now()
            )

            # Update request status
            req.status = 'fulfilled'
            req.save()

            # Update donor score silently — identity never exposed
            donor.reliability_score = min(100, donor.reliability_score + 10)
            donor.total_donations += 1

            # Update member tag based on donations
            if donor.total_donations >= 10:
                donor.member_tag = 'Platinum Donor'
            elif donor.total_donations >= 5:
                donor.member_tag = 'Gold Donor'
            elif donor.total_donations >= 2:
                donor.member_tag = 'Silver Donor'
            else:
                donor.member_tag = 'Bronze Donor'

            donor.save()

            return Response({
                'message': 'Donation verified successfully.',
                'donation': DonationHistorySerializer(donation).data
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


# ════════════════════════════════════════════════════
#  DONOR VIEWS OWN HISTORY
# ════════════════════════════════════════════════════

class DonorHistoryView(APIView):

    def get(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Only donors can view their history.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])
            history = DonationHistory.objects.filter(
                donor=donor
            ).order_by('-donated_at')

            return Response(
                DonationHistorySerializer(history, many=True).data
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ════════════════════════════════════════════════════
#  PARTNER VIEWS RECEIVED DONATIONS
# ════════════════════════════════════════════════════

class PartnerDonationHistoryView(APIView):

    def get(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can view this.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner = Partners.objects.get(id=payload['id'])
            history = DonationHistory.objects.filter(
                partner=partner
            ).order_by('-donated_at')

            return Response(
                DonationHistorySerializer(history, many=True).data
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ════════════════════════════════════════════════════
#  PUBLIC LEADERBOARD
# ════════════════════════════════════════════════════

class DonorLeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Top donors by total donations — anonymous
        top_donors = Donor.objects.filter(
            total_donations__gt=0
        ).order_by('-total_donations')[:10]

        leaderboard = []
        for donor in top_donors:
            leaderboard.append({
                'name': donor.name,
                'total_donations': donor.total_donations,
                'member_tag': donor.member_tag,
                'reliability_score': donor.reliability_score,
                'blood_group': donor.blood_group,
                # No email, phone, address — anonymous ✅
            })

        return Response(leaderboard)