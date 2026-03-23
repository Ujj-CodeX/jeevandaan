from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone


def expire_attender_requests():
    from requests_app.models import AttenderRequest
    expired = AttenderRequest.objects.filter(
        status='pending',
        expires_at__lt=timezone.now()   # expires_at is in the past
    )
    count = expired.count()
    expired.update(status='expired')
    if count > 0:
        print(f"{count} attender requests expired!")

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


def unlock_donor_accounts():
    from users.models import Donor
    unlocked = Donor.objects.filter(
        is_locked=True,
        locked_until__lt=timezone.now()   # lock period is over
    )
    count = unlocked.count()
    unlocked.update(is_locked=False, locked_until=None)
    if count > 0:
        print(f"{count} donor accounts unlocked!")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    # Run every 15 minutes
    scheduler.add_job(
        expire_attender_requests,
        'interval',
        minutes=15,
        id='expire_attender_requests',
        replace_existing=True
    )

    # Run every 15 minutes
    scheduler.add_job(
        expire_donor_requests,
        'interval',
        minutes=15,
        id='expire_donor_requests',
        replace_existing=True
    )

    # Run every hour
    scheduler.add_job(
        unlock_donor_accounts,
        'interval',
        hours=1,
        id='unlock_donor_accounts',
        replace_existing=True
    )

    scheduler.start()
    print("Scheduler started")