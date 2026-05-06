from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone


def expire_unvisited_donor_requests():
    from requests_app.models import PartnerDonorRequest
    from chat.models import Chat
    from datetime import timedelta

    two_hours_ago = timezone.now() - timedelta(hours=2)

    assigned_requests = PartnerDonorRequest.objects.filter(
        status='assigned',
        updated_at__lte=two_hours_ago
    )

    for req in assigned_requests:
        visited = Chat.objects.filter(
            request=req,
            sender_type='donor',
            message__in=['reached', 'donated']
        ).exists()

        if not visited:
            # ── FIX: pehle donor save karo, PHIR None karo ──
            donor = req.assigned_donor  # ← pehle reference lo

            req.status = 'expired'
            req.assigned_donor = None   # ← ab None karo
            req.save()

            # ── Ab donor check karo ──
            if donor:
                donor.reliability_score = max(0, donor.reliability_score - 10)
                donor.cancellation_count += 1

                if donor.cancellation_count >= 3:
                    donor.is_locked = True
                    donor.locked_until = timezone.now() + timedelta(days=30)

                donor.save()
                print(f"Request #{req.id} expired — donor {donor.name} score deducted")


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
        locked_until__lt=timezone.now()
    )
    count = unlocked.count()
    unlocked.update(is_locked=False, locked_until=None)
    if count > 0:
        print(f"{count} donor accounts unlocked!")


def start():
    # ── Guard: table exist karti hai tabhi start karo ──
    try:
        from django.db import connection
        tables = connection.introspection.table_names()
        if 'django_apscheduler_djangojob' not in tables:
            print("⚠️  Scheduler skipped — migrations not run yet")
            return
    except Exception as e:
        print(f"⚠️  Scheduler skipped — {e}")
        return
    
    # so that scheduler can use only one worker
    import os
    if os.environ.get('GUNICORN_WORKER_ID') != '1':
        return
    try:
        from django_apscheduler.models import DjangoJob
        DjangoJob.objects.all().delete()
    except:
        pass

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        expire_attender_requests,
        'interval',
        minutes=15,
        id='expire_attender_requests',
        replace_existing=True
    )

    scheduler.add_job(
        expire_donor_requests,
        'interval',
        minutes=15,
        id='expire_donor_requests',
        replace_existing=True
    )

    scheduler.add_job(
        unlock_donor_accounts,
        'interval',
        hours=1,
        id='unlock_donor_accounts',
        replace_existing=True
    )

    scheduler.add_job(
        expire_unvisited_donor_requests,  # ← FIX: indentation sahi kiya
        'interval',
        minutes=30,
        id='expire_unvisited_donor_requests',
        replace_existing=True
    )

    scheduler.start()
    print("✅ Scheduler started")