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

class DonationCamp(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Who organized
    organizer = models.ForeignKey(
        Partners,
        on_delete=models.CASCADE,
        related_name='organized_camps'
    )

    # Camp details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    location = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6,
        null=True, blank=True
    )

    # Timing
    camp_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Blood groups needed
    blood_groups_needed = models.JSONField(default=list)
    # e.g. ["A+", "O-", "B+"]

    # Expected donors
    expected_donors = models.PositiveIntegerField(default=0)

    # Status
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    # Stock update enforcement
    stock_updated_after_camp = models.BooleanField(default=False)
    dashboard_frozen = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.organizer.hospital_name} on {self.camp_date}"
    
class CampEnrollment(models.Model):

    camp = models.ForeignKey(
        DonationCamp,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    donor = models.ForeignKey(
        'users.Donor',
        on_delete=models.CASCADE,
        related_name='camp_enrollments'
    )

    # Enrollment details
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3)

    # Status
    attended = models.BooleanField(default=False)

    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('camp', 'donor')  # one enrollment per donor per camp

    def __str__(self):
        return f"{self.donor.name} enrolled in {self.camp.title}"