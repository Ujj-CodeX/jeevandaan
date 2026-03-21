from django.db import models

from django.db import models

DEFAULT_MESSAGES = [
    ('on_the_way', 'On my way'),
    ('reached', 'Reached the bank'),
    ('unable_to_come', 'Unable to come'),
    ('delayed', 'Running late'),
    ('donated', 'Donation completed'),
]

SENDER_TYPES = [
    ('donor', 'Donor'),
    ('partner', 'Partner'),
]


class Chat(models.Model):

    # Which donor request this chat belongs to
    request = models.ForeignKey(
        'requests_app.PartnerDonorRequest',
        on_delete=models.CASCADE,
        related_name='chats'
    )

    # Who sent this message
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPES)

    # Only predefined messages allowed — no free text
    message = models.CharField(max_length=20, choices=DEFAULT_MESSAGES)

    # Timestamps
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_type} → {self.get_message_display()} at {self.sent_at}"
