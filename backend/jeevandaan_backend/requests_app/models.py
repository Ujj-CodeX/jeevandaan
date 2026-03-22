
import uuid
from django.db import models
from users.models import Donor

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
    patient_photo = models.ImageField(upload_to='patient_photos/', null=True, blank=True)  # fixed: was patient_photo

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

    doctor_letter_head = models.CharField(max_length=100)
    attnder_id_proof = models.ImageField(upload_to='attender_id_proofs/', null=True, blank=True)  # fixed: was attnder_id_proof

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()  # fixed: was expires_at


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

    cancellation_reason = models.TextField()  # fixed: was cancellation_reason
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.partner.hospital_name} needs {self.quantity} units of {self.blood_group} — {self.status}"
