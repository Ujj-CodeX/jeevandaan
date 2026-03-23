from .sms import send_sms, send_whatsapp
from .models import Notification
from django.utils import timezone


def notify_donor(donor, trigger, message):
    """
    Send SMS + WhatsApp to donor
    Creates notification record in DB
    """
    if not donor.phone_number:
        print(f"No phone number for donor {donor.name}")
        return

    # Send SMS
    sms_success = send_sms(donor.phone_number, message)

    # Create SMS notification record
    Notification.objects.create(
        donor=donor,
        notification_type='sms',
        trigger=trigger,
        message=message,
        status='sent' if sms_success else 'failed',
        sent_at=timezone.now() if sms_success else None
    )

    # Send WhatsApp
    whatsapp_success = send_whatsapp(donor.phone_number, message)

    # Create WhatsApp notification record
    Notification.objects.create(
        donor=donor,
        notification_type='whatsapp',
        trigger=trigger,
        message=message,
        status='sent' if whatsapp_success else 'failed',
        sent_at=timezone.now() if whatsapp_success else None
    )

    # Fallback call if both failed
    if not sms_success and not whatsapp_success:
        Notification.objects.create(
            donor=donor,
            notification_type='call',
            trigger=trigger,
            message=message,
            status='pending',
            is_fallback=True,
            fallback_attempted_at=timezone.now()
        )
        print(f"Fallback call triggered for {donor.name} ⚠️")


def notify_nearby_donors(blood_group, city, message, trigger='donor_request'):
    """
    Find nearby donors and notify them
    """
    from users.models import Donor

    donors = Donor.objects.filter(
        blood_group=blood_group,
        address__icontains=city,
        is_locked=False,
    )

    if not donors.exists():
        print(f"No donors found for {blood_group} in {city}")
        return 0

    count = 0
    for donor in donors:
        notify_donor(donor, trigger, message)
        count += 1

    print(f"Notified {count} donors ✅")
    return count