from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


from .tasks import send_donor_notifications_task
from .models import Notification
from .serializers import NotificationSerializer
from users.models import Donor
from partners.models import Partners
import jwt
import os
from .helpers import notify_nearby_donors

from config.authentication import PartnerJWTAuthentication
from config.permissions import IsPartner

from config.authentication import AnyJWTAuthentication
from config.permissions import IsAuthenticated  







# ── helper — create notification ─────────────────────
def create_notification(donor=None, partner=None, notification_type='sms', trigger='donor_request', message=''):
    return Notification.objects.create(
        donor=donor,
        partner=partner,
        notification_type=notification_type,
        trigger=trigger,
        message=message,
        status='pending'
    )


# ════════════════════════════════════════════════════
#  DONOR NOTIFICATIONS
# ════════════════════════════════════════════════════

class DonorNotificationListView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
            donor = request.user

            
            notifications = Notification.objects.filter(
                donor=donor
            ).order_by('-created_at')

            return Response(
                NotificationSerializer(notifications, many=True).data
            )

        


# ════════════════════════════════════════════════════
#  PARTNER NOTIFICATIONS
# ════════════════════════════════════════════════════

class PartnerNotificationListView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
            partner = request.user

            
            notifications = Notification.objects.filter(
                partner=partner
            ).order_by('-created_at')

            return Response(
                NotificationSerializer(notifications, many=True).data
            )

       


# ════════════════════════════════════════════════════
#  MARK NOTIFICATION AS READ
# ════════════════════════════════════════════════════

class NotifyNearbyDonorsView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        try:
            partner = request.user

            blood_group = request.data.get('blood_group')
            city = request.data.get('city')
            message = request.data.get(
                'message',
                f'Urgent! {blood_group} blood needed near you. Please donate at JeevanDaan!'
            )

            if not blood_group or not city:
                return Response(
                    {'error': 'blood_group and city are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not partner.latitude or not partner.longitude:
                return Response(
                {'error': 'Partner location not set. Update your location first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

            # Send notifications
            send_donor_notifications_task.delay(
            blood_group, str(partner.latitude), str(partner.longitude), message, 10
        )

            return Response({'message': 'Notifications are being sent to nearby donors in the background.'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    

       
class MarkNotificationReadView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            user =  request.user
            

            if isinstance(user, Donor):
                notification = Notification.objects.get(
                    id=notification_id,
                    donor__id=user
                )
            elif isinstance(user, Partners):
                notification = Notification.objects.get(
                    id=notification_id,
                    partner=user
                )

            else:
                return Response(
                    {'error': 'Invalid user type.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            notification.status = 'delivered'
            notification.sent_at = timezone.now()
            notification.save()

            return Response({'message': 'Notification marked as read.'})

        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        