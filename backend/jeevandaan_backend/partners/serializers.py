from rest_framework import serializers
from .models import Partners
import bcrypt


class PartnerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Partners
        fields = [
            'hospital_name', 'email', 'contact',
            'address', 'city', 'state',
            'partner_type', 'facility',
            'license_id', 'convenience_fee',
            'fee_description', 'password'
        ]

    def validate_email(self, value):
        if Partners.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_license_id(self, value):
        if Partners.objects.filter(license_id=value).exists():
            raise serializers.ValidationError("License ID already registered.")
        return value

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()
        return Partners.objects.create(password=hashed, **validated_data)


class PartnerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()         # partners login with email
    password = serializers.CharField(write_only=True)


class PartnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        exclude = ['password']               # never expose password


class PartnerPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = [
            'id', 'hospital_name', 'partner_type',
            'address', 'city', 'state',
            'contact', 'facility',
            'convenience_fee', 'fee_description',
            'latitude', 'longitude',
            'is_verified', 'is_live'
        ]