
import uuid
from django.db import models
from users.models import Donor
import random
import string


class AttenderRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]



    attender = models.ForeignKey(Donor, on_delete=models.CASCADE)  # fixed: was attender_id
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # fixed: was reference_idpatit
    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    patient_photo = models.URLField(max_length=500, blank=True, null=True)      # ← URLField
    doctor_letterhead = models.URLField(max_length=500, blank=True, null=True)  # ← URLField
    attender_id_proof = models.URLField(max_length=500, blank=True, null=True)

    fulfilled_by = models.ForeignKey(      
        'partners.Partners',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='fulfilled_attender_requests'
    )

    quantity = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='normal')
    hospital_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    doctor_phone = models.CharField(max_length=15 , null=True, blank=True)  # fixed: was doctor_phone
    attender_name = models.CharField(max_length=100)
    attender_phone = models.CharField(max_length=15)  # fixed: was attender_phone
    id_type = models.CharField(max_length=50)
    id_no = models.CharField(max_length=50)
    city = models.CharField(max_length=100, blank=True, null=True)


    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # fixed: was expires_at


def __str__(self):
    return f"Request {self.reference_id} for {self.patient_name} ({self.blood_group}) at {self.hospital_name}"

class PartnerDonorRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),           # visible to all nearby donors
        ('assigned', 'Assigned'),   # donor accepted
        ('fulfilled', 'Fulfilled'), # donation done, bank verified
        ('expired', 'Expired'),     # no donor responded in time
        ('cancelled', 'Cancelled'), # bank cancelled the request
    ]

    partner = models.ForeignKey('partners.Partners', on_delete=models.CASCADE) 
    
    assigned_donor = models.ForeignKey('users.Donor', on_delete=models.SET_NULL, null=True, blank=True) 
     # fixed: was assigned_donor_id

    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    expires_at = models.DateTimeField()  # fixed: was expires_at

    cancellation_reason = models.TextField(null=True, blank=True)  # fixed: was cancellation_reason
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.partner.hospital_name} needs {self.quantity} units of {self.blood_group} — {self.status}"



class OTPCode(models.Model):

    # Linked to donor request
    request = models.OneToOneField(
        PartnerDonorRequest,
        on_delete=models.CASCADE,
        related_name='otp'
    )

    # The OTP code
    code = models.CharField(max_length=6, unique=True)

    # Is it used?
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP {self.code} for Request #{self.request.id}"

    @staticmethod
    def generate_code():
        """Generate unique 6 digit OTP"""
        while True:
            code = ''.join(random.choices(string.digits, k=6))
            if not OTPCode.objects.filter(code=code).exists():
                return code

            

    
class InterPartnerRequest(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('fulfilled', 'Fulfilled'),
        ('rejected', 'Rejected'),
    ]

    # Bank A requests Bank B
    requesting_partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.CASCADE,
        related_name='inter_requests_sent'
    )
    fulfilling_partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.CASCADE,
        related_name='inter_requests_received'
    )

    # Linked to original attender request
    attender_request = models.ForeignKey(
        AttenderRequest,
        on_delete=models.CASCADE,
        related_name='inter_partner_requests'
    )

    # Blood requirement
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()

    # Fee — Bank A pays Bank B
    convenience_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    # Status
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requesting_partner.hospital_name} → {self.fulfilling_partner.hospital_name} | {self.blood_group}"
class AttenderRating(models.Model):
    COMPLAINT_TYPES = [
        ('exchange_condition', 'Asked for blood exchange'),
        ('overcharging', 'Charged extra fees'),
        ('misbehavior', 'Staff misbehavior'),
        ('fake_stock', 'Wrong stock shown'),
        ('other', 'Other'),
    ]

    # Attender rates partner
    attender = models.ForeignKey(
        'users.Donor',
        on_delete=models.CASCADE,
        related_name='ratings_given'
    )
    partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.CASCADE,
        related_name='ratings_received', null=True, blank=True
    )
    request = models.OneToOneField(
        AttenderRequest,
        on_delete=models.CASCADE,
        related_name='rating'
    )

    # Rating
    stars = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    review = models.TextField(blank=True, null=True)

    # Complaint
    has_complaint = models.BooleanField(default=False)
    complaint_type = models.CharField(
        max_length=50,
        choices=COMPLAINT_TYPES,
        blank=True, null=True
    )
    complaint_detail = models.TextField(blank=True, null=True)
    complaint_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('investigating', 'Investigating'),
            ('resolved', 'Resolved'),
            ('dismissed', 'Dismissed'),
        ],
        default='pending'
    )
    fulfilled_by = models.ForeignKey(
        'partners.Partners',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='fulfilled_requests'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attender.name} → {self.partner.hospital_name} {self.stars}⭐"

class DonorRating(models.Model):
    # Partner rates donor
    partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.CASCADE,
        related_name='donor_ratings_given'
    )
    donor = models.ForeignKey(
        'users.Donor',
        on_delete=models.CASCADE,
        related_name='ratings_received'
    )
    request = models.OneToOneField(
        PartnerDonorRequest,
        on_delete=models.CASCADE,
        related_name='donor_rating'
    )

    stars = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.partner.hospital_name} → Donor {self.stars}⭐"