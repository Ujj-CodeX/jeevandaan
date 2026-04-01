from django.db import models

DEFAULT_MESSAGES = [
    ('on_the_way', 'On my way'),
    ('reached', 'Reached the bank'),
    ('unable_to_come', 'Unable to come'),
    ('delayed', 'Running late'),
    ('donated', 'Donation completed'),
    ('otp_generated', 'OTP Generated'),  # ← add this
]

SENDER_TYPES = [
    ('donor', 'Donor'),
    ('partner', 'Partner'),
    ('system', 'System'),    # ← add this
]


class Chat(models.Model):
    request = models.ForeignKey(
        'requests_app.PartnerDonorRequest',
        on_delete=models.CASCADE,
        related_name='chats'
    )
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPES)
    message = models.CharField(max_length=20, choices=DEFAULT_MESSAGES)
    otp_code = models.CharField(max_length=6, blank=True, null=True)  # ← add
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_type} → {self.get_message_display()} at {self.sent_at}"