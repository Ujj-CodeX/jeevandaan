from django.db import models


class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128 , null=True,blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS) 
    google_id = models.CharField(max_length=255 , unique=True , null=True,blank=True) # fixed: was blood_Group
    auth_provider = models.CharField(max_length=50, choices=[('google', 'Google'), ('local', 'Local')], default='local')  # fixed: was auth_provider
    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class Partners(models.Model):
    hospital_name = models.CharField(max_length=100)   # fixed: was Hospital_name
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)          # fixed: was Contact
    address = models.TextField()
    facility = models.TextField()                      # fixed: was Facility
    license_id = models.CharField(max_length=50, unique=True)  # fixed: was L_id
    password = models.CharField(max_length=128)

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
    
