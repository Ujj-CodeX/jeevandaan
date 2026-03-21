from django.db import models



class DonationHistory(models.Model):

    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    # Who donated — ForeignKey not exposed to attender/patient
    donor = models.ForeignKey(
        'users.Donor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donation_history'
    )

    # Which bank received the donation
    partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_donations'
    )

    # Which partner request triggered this donation
    request = models.ForeignKey(
        'requests_app.PartnerDonorRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donation_records'
    )

    # Donation details
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units_donated = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='completed')

    # Scoring impact — silently updated in backend
    score_change = models.FloatField(default=0.0)  # +ve for donation, -ve for cancellation
    cancellation_reason = models.TextField(null=True, blank=True)

    # Verified by bank
    is_verified_by_bank = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    donated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation — {self.blood_group} {self.units_donated} units — {self.status}"