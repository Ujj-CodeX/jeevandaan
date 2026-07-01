from celery import shared_task
from django.utils import timezone
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

@shared_task

def auto_complete_expired_camps():
    from .models import DonationCamp  # Import here to avoid circular imports

    now = timezone.localtime(timezone.now())
    today = now.date()
    current_time = now.time()

    expired = DonationCamp.objects.filter(
        status__in=['scheduled', 'ongoing']
    ).filter(
        Q(camp_date__lt=today) | Q(camp_date=today, end_time__lt=current_time)
    )

    count = expired.count()

    if count:
        expired.update(status='completed')
        logger.info("camps_auto_completed", extra={'count': count})

    return count