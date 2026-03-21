from rest_framework import serializers
from .models import Donor
import bcrypt

class DonorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Donor
        fields = [
            'name', 'email', 'username',
            'phone_number', 'address',
            'blood_group', 'password'
        ]

        def validate_email(self, value):
            if Donor.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email is already registered.")
            return value
        def validate_username(self, value):
            if Donor.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username is already taken.")
            return value
        def create(self, validated_data):
            raw_password = validated_data.pop('password')
            hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt().decode())
            return Donor.objects.create(password=hashed.decode(), **validated_data)
        

class DonorLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)


class DonorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        exclude = ['password', 'aadhaar_number']

        

        

         