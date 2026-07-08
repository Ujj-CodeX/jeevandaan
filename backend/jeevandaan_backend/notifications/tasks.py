from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_donor_notifications_task(self, blood_group, partner_lat, partner_lng, message, radius_km=10):
    from notifications.helpers import notify_nearby_donors
    try:
        return notify_nearby_donors(blood_group, partner_lat, partner_lng, message, radius_km)
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def notify_camp_donors_task(self, camp_id):
    from partners.models import DonationCamp
    from notifications.helpers import notify_camp_donors
    try:
        camp = DonationCamp.objects.get(id=camp_id)
        return notify_camp_donors(camp)
    except DonationCamp.DoesNotExist:
        return 0
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=15)
def create_notification_task(self, partner_id=None, donor_id=None,
                              notification_type='sms', trigger='donor_request',
                              message='', status='pending'):
    from notifications.models import Notification
    try:
        Notification.objects.create(
            partner_id=partner_id,
            donor_id=donor_id,
            notification_type=notification_type,
            trigger=trigger,
            message=message,
            status=status,
        )
    except Exception as exc:
        raise self.retry(exc=exc)