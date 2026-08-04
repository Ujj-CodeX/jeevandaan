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
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode() 
        return Donor.objects.create(password=hashed, **validated_data)
        

class DonorLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)


class DonorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        exclude = ['password', 'aadhaar_number']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ['name', 'phone_number', 'address', 'blood_group']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()

    def validate_phone_number(self, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def validate_blood_group(self, value):
        donor = self.instance
        if donor and donor.is_aadhaar_verified and value != donor.blood_group:
            raise serializers.ValidationError(
                "Blood group cannot be changed after Aadhaar verification."
            )
        return value      

        

         