from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer
from users.models import Donor
from partners.models import Partners
import jwt
import os
from .helpers import notify_nearby_donors



# ── helper ───────────────────────────────────────────
def decode_token(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])


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

    def get(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'donor':
                return Response(
                    {'error': 'Unauthorized.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            donor = Donor.objects.get(id=payload['id'])
            notifications = Notification.objects.filter(
                donor=donor
            ).order_by('-created_at')

            return Response(
                NotificationSerializer(notifications, many=True).data
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ════════════════════════════════════════════════════
#  PARTNER NOTIFICATIONS
# ════════════════════════════════════════════════════

class PartnerNotificationListView(APIView):

    def get(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Unauthorized.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner = Partners.objects.get(id=payload['id'])
            notifications = Notification.objects.filter(
                partner=partner
            ).order_by('-created_at')

            return Response(
                NotificationSerializer(notifications, many=True).data
            )

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ════════════════════════════════════════════════════
#  MARK NOTIFICATION AS READ
# ════════════════════════════════════════════════════

class NotifyNearbyDonorsView(APIView):

    def post(self, request):
        try:
            payload = decode_token(request)
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can trigger notifications.'},
                    status=status.HTTP_403_FORBIDDEN
                )

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

            # Send notifications
            count = notify_nearby_donors(blood_group, city, message)

            if count == 0:
                return Response(
                    {'error': 'No nearby donors found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({
                'message': f'Notifications sent to {count} nearby donors.',
                'donors_notified': count
            })

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
class MarkNotificationReadView(APIView):

    def post(self, request, notification_id):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            sender_type = payload.get('type')

            if sender_type == 'donor':
                notification = Notification.objects.get(
                    id=notification_id,
                    donor__id=payload['id']
                )
            else:
                notification = Notification.objects.get(
                    id=notification_id,
                    partner__id=payload['id']
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
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)