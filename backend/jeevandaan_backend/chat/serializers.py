from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    message_display = serializers.CharField(
        source='get_message_display',
        read_only=True
    )

    class Meta:
        model = Chat
        fields = [
            'id',
            'request',
            'sender_type',
            'message',
            'message_display',
            'otp_code',        # ← add
            'sent_at'
        ]
        read_only_fields = [
            'sender_type',
            'sent_at',
            'otp_code'
        ]