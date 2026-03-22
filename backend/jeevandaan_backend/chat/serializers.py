from rest_framework import serializers
from .models import Chat 

class ChatSerializer(serializers.ModelSerializer):
    message_display = serializers.CharField(source='get_message_display', read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'request', 'sender_type', 'message', 'sent_at', 'message_display']

        read_only_fields = [ 'sent_at', 'sender_type']
        
