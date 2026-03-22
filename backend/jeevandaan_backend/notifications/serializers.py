from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'trigger',
            'message',
            'status',
            'is_fallback',
            'created_at',
            'sent_at'
        ]
        read_only_fields = [
            'status',
            'is_fallback',
            'created_at',
            'sent_at'
        ]