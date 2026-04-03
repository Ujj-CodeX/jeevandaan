
from datetime import date
from .models import DonationCamp

def get_partner_lock_status(partner):
    """
    Returns True if the partner has a camp today 
    that hasn't been marked as 'stock_updated_after_camp'.
    """
    today = date.today()
    
    # Check for any camp today that isn't updated yet
    frozen_camp_exists = DonationCamp.objects.filter(
        organizer=partner,
        camp_date=today,
        stock_updated_after_camp=False
    ).exists()

    return frozen_camp_exists