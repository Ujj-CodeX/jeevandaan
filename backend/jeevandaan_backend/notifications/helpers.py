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


from geopy.distance import geodesic

def notify_nearby_donors(blood_group, partner_lat, partner_lng, message, radius_km=10):
    """
    Find donors within radius_km of partner location
    and notify them via SMS + WhatsApp
    """
    from users.models import Donor

    # Get all matching blood group donors
    donors = Donor.objects.filter(
        blood_group=blood_group,
        is_locked=False,
        latitude__isnull=False,    # ← must have GPS location
        longitude__isnull=False,
    )

    notified = 0
    for donor in donors:
        try:
            donor_location = (float(donor.latitude), float(donor.longitude))
            partner_location = (float(partner_lat), float(partner_lng))

            # Calculate distance
            distance = geodesic(partner_location, donor_location).km

            if distance <= radius_km:
                # Within range — notify!
                notify_donor(
                    donor=donor,
                    trigger='donor_request',
                    message=f"{message} — {round(distance, 1)}km from you"
                )
                notified += 1

        except Exception as e:
            print(f"Error notifying donor {donor.id}: {e}")
            continue

    print(f"Notified {notified} donors within {radius_km}km ✅")
    return notified

def notify_camp_donors(camp):
    from users.models import Donor
    from users.location import get_nearby_donors

    donors = Donor.objects.filter(
        is_locked=False,
        latitude__isnull=False,
        longitude__isnull=False
    )

    if camp.blood_groups_needed:
        donors = donors.filter(
            blood_group__in=camp.blood_groups_needed
        )

    nearby = get_nearby_donors(
        camp.latitude,
        camp.longitude,
        donors,
        radius_km=20
    )

    message = f"A nearby blood donation camp is scheduled at {camp.location} on {camp.camp_date}. Timings: {camp.start_time}–{camp.end_time}. Enroll now via Dashboard!"
    notified = 0

    for item in nearby:
        donor = item['donor']   

        notify_donor(
            donor=donor,
            trigger='camp_notification',
            message=message
        )

        notified += 1

    return notified