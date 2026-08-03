from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone

from celery import shared_task

from notifications.tasks import create_notification_task

@shared_task
def expire_unvisited_donor_requests():
    from requests_app.models import PartnerDonorRequest
    from chat.models import Chat
    from notifications.tasks import create_notification_task
    from datetime import timedelta

    # ── FIX: reduced from 2 hours to 1 hour
    one_hour_ago = timezone.now() - timedelta(hours=1)

    assigned_requests = PartnerDonorRequest.objects.select_related('partner').filter(
        status='assigned',
        updated_at__lte=one_hour_ago
    )

    for req in assigned_requests:
        visited = Chat.objects.filter(
            request=req,
            sender_type='donor',
            message__in=['reached', 'donated']
        ).exists()

        if not visited:
            donor = req.assigned_donor

            req.status = 'expired'
            req.assigned_donor = None
            req.save()

            # ── FIX: notify partner that the assigned donor didn't show up
            create_notification_task.delay(
                partner_id=req.partner_id,
                notification_type='sms',
                trigger='request_expiry',
                message=(
                    f'Your {req.blood_group} request ({req.quantity} units) '
                    f'has expired — the assigned donor did not arrive within 1 hour.'
                ),
                status='pending',
            )

            if donor:
                donor.reliability_score = max(0, donor.reliability_score - 10)
                donor.cancellation_count += 1

                if donor.cancellation_count >= 3:
                    donor.is_locked = True
                    donor.locked_until = timezone.now() + timedelta(days=30)

                donor.save()
                print(f"Request #{req.id} expired — donor {donor.name} score deducted")

@shared_task
def expire_attender_requests():
    from requests_app.models import AttenderRequest
    expired = AttenderRequest.objects.filter(
        status='pending',
        expires_at__lt=timezone.now()
    )
    count = expired.count()
    expired.update(status='expired')
    if count > 0:
        print(f"{count} attender requests expired!")

@shared_task
def expire_donor_requests():
    from requests_app.models import PartnerDonorRequest
    expired = PartnerDonorRequest.objects.filter(
        status='open',
        expires_at__lt=timezone.now()
    )
    count = expired.count()
    expired.update(status='expired')
    if count > 0:
        print(f"{count} donor requests expired!")

@shared_task
def unlock_donor_accounts():
    from users.models import Donor
    unlocked = Donor.objects.filter(
        is_locked=True,
        locked_until__lt=timezone.now()
    )
    count = unlocked.count()
    unlocked.update(is_locked=False, locked_until=None)
    if count > 0:
        print(f"{count} donor accounts unlocked!") 


