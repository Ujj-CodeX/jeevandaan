from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='partner.hospital_name', read_only=True)
    city = serializers.CharField(source='partner.city', read_only=True)
    latitude = serializers.CharField(source='partner.latitude', read_only=True)
    longitude = serializers.CharField(source='partner.longitude', read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id', 'blood_group', 'quantity',
            'hospital_name', 'city',
            'latitude', 'longitude',
            'updated_at'
        ]