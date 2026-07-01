from django.db import models



class Stock(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    
    partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.CASCADE,
        related_name='stock'
    )

    
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    quantity = models.PositiveIntegerField(default=0)

    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # One entry per blood group per partner
        unique_together = ('partner', 'blood_group')

    def __str__(self):
        return f"{self.partner.hospital_name} — {self.blood_group}: {self.quantity} units"




class StockUpdateLog(models.Model):
    
    partner = models.ForeignKey(
        'partners.Partners',
        on_delete=models.CASCADE,
        related_name='stock_update_logs'
    )
    blood_group = models.CharField(max_length=3, choices=Stock.BLOOD_GROUPS)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.partner.hospital_name} updated {self.blood_group} → {self.quantity} @ {self.created_at}"