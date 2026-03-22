from django.db import models


class Partners(models.Model):

    PARTNER_TYPES = [
        ('government', 'Government'),
        ('private_multi_specialty', 'Private Multi-Specialty'),
        ('blood_bank', 'Blood Bank'),
    ]

    # Basic info
    hospital_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPES)  # ← only once
    facility = models.TextField(blank=True, null=True)                     # ← added back

    # Auth
    password = models.CharField(max_length=128)

    # Verification
    license_id = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    # Charges
    convenience_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fee_description = models.TextField(blank=True, null=True)

    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hospital_name