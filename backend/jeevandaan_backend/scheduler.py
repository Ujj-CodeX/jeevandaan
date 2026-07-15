from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone

from celery import shared_task

from config.logger import get_logger
 

logger = get_logger(__name__)

@shared_task
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

    total = assigned_requests.count()
    expired = 0
    locked = 0

    logger.info("expire_unvisited_donor_requests_started", extra={"total_assigned_requests": total})

    for req in assigned_requests:
        try:
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

                expired += 1

                # ── FIX: notify partner about the expiry
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
                        locked += 1

                        logger.warning("donor_account_locked_by_scheduler", extra={
                            "donor_id": donor.id, "cancellation_count": donor.cancellation_count,
                            "locked_until": str(donor.locked_until), "request_id": req.id,
                        })
                    donor.save()

                    logger.info("donor_score_deducted_unvisited", extra={
                        "donor_id": donor.id, "request_id": req.id,
                        "new_score": donor.reliability_score,
                        "cancellation_count": donor.cancellation_count,
                    })
        except Exception:
            logger.exception("expired_unvisited_request_error", extra={"request_id": req.id})
            continue

    logger.info("expire_unvisited_donor_requests_completed", extra={
        "total_checked": total, "expired": expired, "donors_locked": locked,
    })

@shared_task
def expire_attender_requests():
    from requests_app.models import AttenderRequest

    logger.info("expire_attender_requests_started")
    

    try:
        expired = AttenderRequest.objects.filter(
        status='pending',
        expires_at__lt=timezone.now()
        )
        count = expired.count()
        expired.update(status='expired')

        logger.info("expire_attender_requests_completed", extra={"expired_count": count})
    
    except Exception :
        logger.exception("expire_attender_requests_error")   
    

@shared_task
def expire_donor_requests():
    from requests_app.models import PartnerDonorRequest


    logger.info("expire_donor_requests_started")
    try:
        expired = PartnerDonorRequest.objects.filter(
        status='open',
        expires_at__lt=timezone.now()
        )
        count = expired.count()
        expired.update(status='expired')

        logger.info("expire_donor_requests_completed", extra={"expired_count": count})
    except Exception :
        logger.exception("expire_donor_requests_error")

@shared_task
def unlock_donor_accounts():
    from users.models import Donor

    logger.info("unlock_donor_accounts_started")

    try:
        unlocked = Donor.objects.filter(
         is_locked=True,
         locked_until__lt=timezone.now()
        )
        count = unlocked.count()
        unlocked.update(is_locked=False, locked_until=None)
        logger.info("unlock_donor_accounts_completed", extra={"unlocked_count": count})
    except Exception :      
        logger.exception("unlock_donor_accounts_error")
