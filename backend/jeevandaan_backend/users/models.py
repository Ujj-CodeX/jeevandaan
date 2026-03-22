from django.db import models

class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    AUTH_PROVIDERS = [
        ('google', 'Google'),('local', 'Local')]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128 , null=True,blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS) 
    google_id = models.CharField(max_length=255 , unique=True , null=True,blank=True) # fixed: was blood_Group
    auth_provider = models.CharField(max_length=50, choices=[('google', 'Google'), ('local', 'Local')], default='local') 
    
    aadhaar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)  # fixed: was aadhar_number
    is_verified = models.BooleanField(default=False) 
    verification_tag = models.BooleanField(default=False) 
    

    reliability_score = models.FloatField(default=0.0)  # fixed: was reliability_score
    total_donations = models.PositiveIntegerField(default=0)  # fixed: was
    member_tag = models.CharField(max_length=50, default='New Member')
    cancellation_count = models.PositiveIntegerField(default=0) 
    is_locked=models.BooleanField(default=False)
    locked_until=models.DateTimeField(null=True, blank=True)
    
    total_requests_raised = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)



    def __str__(self):
        return f"{self.name} ({self.blood_group})"
