from rest_framework import serializers
from .models import DonationHistory


class DonationHistorySerializer(serializers.ModelSerializer):
    donor_name = serializers.CharField(
        source='donor.name',
        read_only=True
    )
    hospital_name = serializers.CharField(
        source='partner.hospital_name',
        read_only=True
    )

    class Meta:
        model = DonationHistory
        fields = [
            'id',
            'donor_name',        # name only — no other donor details
            'hospital_name',
            'blood_group',
            'units_donated',
            'status',
            'score_change',
            'is_verified_by_bank',
            'verified_at',
            'donated_at',
        ]
        read_only_fields = [
            'donor_name',
            'hospital_name',
            'score_change',
            'is_verified_by_bank',
            'verified_at',
            'donated_at',
        ]