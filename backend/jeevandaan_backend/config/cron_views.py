# config/cron_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
import os


def verify_cron_secret(request):
    secret = request.headers.get('X-Cron-Secret', '')
    return secret == os.getenv('CRON_SECRET', '')


class ExpireAttenderRequestsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not verify_cron_secret(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        from requests_app.models import AttenderRequest
        expired = AttenderRequest.objects.filter(
            status='pending',
            expires_at__lt=timezone.now()
        )
        count = expired.count()
        expired.update(status='expired')
        return Response({'expired_attender_requests': count})


class ExpireDonorRequestsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not verify_cron_secret(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        from requests_app.models import PartnerDonorRequest
        expired = PartnerDonorRequest.objects.filter(
            status='open',
            expires_at__lt=timezone.now()
        )
        count = expired.count()
        expired.update(status='expired')
        return Response({'expired_donor_requests': count})


class UnlockDonorAccountsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not verify_cron_secret(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        from users.models import Donor
        unlocked = Donor.objects.filter(
            is_locked=True,
            locked_until__lt=timezone.now()
        )
        count = unlocked.count()
        unlocked.update(is_locked=False, locked_until=None)
        return Response({'unlocked_donors': count})


class ExpireUnvisitedDonorRequestsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        if not verify_cron_secret(request):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        from requests_app.models import PartnerDonorRequest
        from chat.models import Chat

        two_hours_ago = timezone.now() - timedelta(hours=2)
        assigned_requests = PartnerDonorRequest.objects.filter(
            status='assigned',
            updated_at__lte=two_hours_ago
        ).select_related('assigned_donor')  # ← fetch donor BEFORE nulling

        count = 0
        for req in assigned_requests:
            visited = Chat.objects.filter(
                request=req,
                sender_type='donor',
                message__in=['reached', 'donated']
            ).exists()

            if not visited:
                donor = req.assigned_donor  # ← grab BEFORE nulling
                req.status = 'expired'
                req.assigned_donor = None
                req.save()
                count += 1

                if donor:  # ← now this check is safe
                    donor.reliability_score = max(0, donor.reliability_score - 10)
                    donor.cancellation_count += 1
                    if donor.cancellation_count >= 3:
                        donor.is_locked = True
                        donor.locked_until = timezone.now() + timedelta(days=30)
                    donor.save()

        return Response({'expired_unvisited_requests': count})