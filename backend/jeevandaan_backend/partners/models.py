from django.db import models

class Partners(models.Model):

    PARTNER_TYPES = [
        ('government', 'Government'), ('private multi-specialty', 'Private Multi-Specialty'), ('blood-bank', 'BLOOD BANK')
    ]

    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPES)
    hospital_name = models.CharField(max_length=100)   # fixed: was Hospital_name
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)          # fixed: was Contact
    address = models.TextField()
    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPES)                      # fixed: was Facility
    license_id = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    convenience_fees = models.FloatField(max_digits=10, decimal_places=2, default=0.0)  # fixed: was convenience_fees
    fees_description = models.TextField(blank=True, null=True) 
    
    
    password = models.CharField(max_length=128)

     # Location (for map + nearest search)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.hospital_name


class DonationHistory(models.Model):    # fixed: typo + PascalCase
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)      # fixed: was donor_id
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    date = models.DateField()
    total_donations = models.PositiveIntegerField()
    reliability_score = models.FloatField()
    member_tag = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.donor.name} donated to {self.partner.hospital_name} on {self.date}"


class RaisedRequest(models.Model):
    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    hospital_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    attenders_name = models.CharField(max_length=100)
    attender_phone_number = models.CharField(max_length=15)
    id_type = models.CharField(max_length=50)
    id_no = models.CharField(max_length=50)
    letter_head = models.CharField(max_length=100)
    patient_photo = models.ImageField(upload_to='patient_photos/')  # fixed: added upload_to
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        
        return f"Request for {self.quantity} units of {self.blood_group} at {self.hospital_name} on {self.date}"


class Stock(models.Model):             
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.partner.hospital_name} has {self.quantity} units of {self.blood_group} blood"
    
