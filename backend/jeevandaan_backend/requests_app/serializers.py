from rest_framework import serializers
from .models import AttenderRequest, PartnerDonorRequest


class AttenderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttenderRequest
        fields = '__all__'
        read_only_fields = [
            'reference_id',
            'status',
            'attender',
            'created_at',
            'updated_at'
        ]


class AttenderRequestPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttenderRequest
        fields = [
            'reference_id',
            'blood_group',
            'quantity',
            'urgency',
            'hospital_name',
            'city',
            'status',
            'created_at',
            'expires_at'
        ]


class PartnerDonorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerDonorRequest
        fields = '__all__'
        read_only_fields = [
            'status',
            'partner',
            'assigned_donor',
            'created_at',
            'updated_at'
        ]


class PartnerDonorRequestPublicSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(
        source='partner.hospital_name',
        read_only=True
    )
    city = serializers.CharField(
        source='partner.city',
        read_only=True
    )

    class Meta:
        model = PartnerDonorRequest
        fields = [
            'id',
            'blood_group',
            'quantity',
            'status',
            'hospital_name',
            'city',
            'expires_at',
            'created_at'
        ]