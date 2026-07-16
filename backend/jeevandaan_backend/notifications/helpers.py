from .sms import send_sms, send_whatsapp
from .models import Notification
from django.utils import timezone

from config.logger import get_logger
 

logger = get_logger(__name__)


def notify_donor(donor, trigger, message, notifications_batch=None):
    """
    Send SMS + WhatsApp to donor.
    If notifications_batch (list) is passed, Notification objects are
    appended to it instead of saved individually — caller does bulk_create.
    """
    if not donor.phone_number:
        logger.warning("donor_no_phone", extra={"donor_id": donor.id, "trigger": trigger})
        return False

    sms_success = send_sms(donor.phone_number, message)
    notif_objects = [
        Notification(
            donor=donor, notification_type='sms', trigger=trigger,
            message=message, status='sent' if sms_success else 'failed',
            sent_at=timezone.now() if sms_success else None
        )
    ]

    whatsapp_success = send_whatsapp(donor.phone_number, message)
    notif_objects.append(
        Notification(
            donor=donor, notification_type='whatsapp', trigger=trigger,
            message=message, status='sent' if whatsapp_success else 'failed',
            sent_at=timezone.now() if whatsapp_success else None
        )
    )

    if not sms_success and not whatsapp_success:
        notif_objects.append(
            Notification(
                donor=donor, notification_type='call', trigger=trigger,
                message=message, status='pending',
                is_fallback=True, fallback_attempted_at=timezone.now()
            )
        )
        logger.warning("sms_whatapp_both_failed_fallback_triggered", extra={"donor_id": donor.id, "trigger": trigger})

    if notifications_batch is not None:
        notifications_batch.extend(notif_objects)
    else:
        Notification.objects.bulk_create(notif_objects)

    return sms_success or whatsapp_success


def notify_nearby_donors(blood_group, partner_lat, partner_lng, message, radius_km=10):
    from users.models import Donor

    donors = Donor.objects.filter(
        blood_group=blood_group, is_locked=False,
        latitude__isnull=False, longitude__isnull=False,
    )

    total_checked = 0
    notified = 0
    failed = 0
    notifications_batch = []   # ← accumulate here

    logger.info("notifying_nearby_donors_started", extra={"blood_group": blood_group, "radius_km": radius_km})

    for donor in donors:
        total_checked += 1
        try:
            donor_location = (float(donor.latitude), float(donor.longitude))
            partner_location = (float(partner_lat), float(partner_lng))
            distance = geodesic(partner_location, donor_location).km

            if distance <= radius_km:
                notify_donor(
                    donor=donor, trigger='donor_request',
                    message=f"{message} — {round(distance, 1)}km from you",
                    notifications_batch=notifications_batch,   # ← individual create() ki jagah
                )
                notified += 1
        except Exception:
            failed += 1
            logger.exception("donor_notify_error", extra={"donor_id": donor.id})
            continue

    if notifications_batch:
        Notification.objects.bulk_create(notifications_batch)   # ← ek hi batch INSERT

    logger.info("notify_nearby_donors_completed", extra={
        "blood_group": blood_group, "radius_km": radius_km,
        "total_checked": total_checked, "notified": notified, "failed": failed,
    })
    return notified