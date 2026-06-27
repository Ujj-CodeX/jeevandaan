from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('call', 'Call'),          # fallback if sms/whatsapp fails
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),     # not sent yet
        ('sent', 'Sent'),           # successfully sent
        ('failed', 'Failed'),       # delivery failed
        ('delivered', 'Delivered'), # confirmed delivered
    ]

    TRIGGER_CHOICES = [
        ('donor_request', 'Donor Request'),         # bank pinging nearby donors
        ('request_expiry', 'Request Expiry'),       # request about to expire
        ('request_fulfilled', 'Request Fulfilled'), # request fulfilled
        ('donor_accepted', 'Donor Accepted'),       # donor accepted request
        ('bank_verified', 'Bank Verified'),         # bank verified donation
        ('score_updated', 'Score Updated'),         # donor score changed
        ('account_locked', 'Account Locked'),
        ('password_reset', 'Password Reset'),       # donor account locked
    ]

    donor = models.ForeignKey('users.Donor', related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)  # who receives the notification
    partner = models.ForeignKey('partners.Partners', related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)  # which partner triggered it (if applicable)
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    trigger = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    

    is_fallback = models.BooleanField(default=False)  # true if this is a fallback notification (e.g. call after sms/whatsapp failure)
    fallback_attempted = models.BooleanField(default=False)  # true if we've already attempted the fallback method

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)  # when the notification was actually sent

    def __str__(self):
        recipient = self.donor or self.partner
        return f"Notification to {recipient} - {self.notification_type} - {self.trigger} - {self.status}"
