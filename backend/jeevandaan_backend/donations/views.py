from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.utils import timezone
from .models import DonationHistory
from .serializers import DonationHistorySerializer
from users.models import Donor
from partners.models import Partners
from requests_app.models import PartnerDonorRequest
import jwt
import os
from config.authentication import PartnerJWTAuthentication
from config.permissions import IsPartner
from config.authentication import DonorJWTAuthentication
from config.permissions import IsDonor



# ── helper ───────────────────────────────────────────



# ════════════════════════════════════════════════════
#  BANK VERIFIES DONATION
# ════════════════════════════════════════════════════

from django.db import transaction
from django.db.models import F
from django.db.models.functions import Least

class VerifyDonationView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request, request_id):
        try:
            partner = request.user
            with transaction.atomic():
                req = PartnerDonorRequest.objects.select_for_update().get(
                    id=request_id,
                    partner=partner,
                    status="assigned"
                )

                donor = req.assigned_donor

                # Create donation history
                donation = DonationHistory.objects.create(
                    donor=donor,
                    partner=partner,
                    request=req,
                    blood_group=req.blood_group,
                    units_donated=req.quantity,
                    status="completed",
                    score_change=10.0,
                    is_verified_by_bank=True,
                    verified_at=timezone.now()
                )

                # Update request status
                req.status = "fulfilled"
                req.save(update_fields=["status"])

                # Atomic donor update
                Donor.objects.filter(pk=donor.pk).update(
                    reliability_score=Least(F("reliability_score") + 10, 100),
                    total_donations=F("total_donations") + 1,
                )

                donor.refresh_from_db(fields=["reliability_score", "total_donations"])

                # Update member tag
                if donor.total_donations >= 10:
                    donor.member_tag = "Platinum Donor"
                elif donor.total_donations >= 5:
                    donor.member_tag = "Gold Donor"
                elif donor.total_donations >= 2:
                    donor.member_tag = "Silver Donor"
                else:
                    donor.member_tag = "Bronze Donor"

                donor.save(update_fields=["member_tag"])

            return Response({
                'message': 'Donation verified successfully.',
                'donation': DonationHistorySerializer(donation).data
            })

        except PartnerDonorRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        


# ════════════════════════════════════════════════════
#  DONOR VIEWS OWN HISTORY
# ════════════════════════════════════════════════════

class DonorHistoryView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]



    def get(self, request):
            donor = request.user
            history = DonationHistory.objects.filter(
                donor=donor
            ).select_related('partner', 'request').order_by('-donated_at')

            return Response(
                DonationHistorySerializer(history, many=True).data
            )

        

# ════════════════════════════════════════════════════
#  PARTNER VIEWS RECEIVED DONATIONS
# ════════════════════════════════════════════════════

class PartnerDonationHistoryView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        
            

            partner = request.user
            history = DonationHistory.objects.filter(
                partner=partner
            ).select_related('donor', 'request').order_by('-donated_at')

            return Response(
                DonationHistorySerializer(history, many=True).data
            )

# ════════════════════════════════════════════════════
#  PUBLIC LEADERBOARD
# NOT IN USE RIGHT NOW, BUT CAN BE USED FOR FUTURE
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
                # No email, phone, address — anonymous  
            })

        return Response(leaderboard)