from rest_framework import serializers
from .models import Partners
import bcrypt
from .models import DonationCamp, CampEnrollment

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
    license_id = serializers.CharField()
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



class DonationCampSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(
        source='organizer.hospital_name',
        read_only=True
    )
    enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = DonationCamp
        fields = [
            'id', 'title', 'description',
            'location', 
            'camp_date', 'start_time', 'end_time',
            'blood_groups_needed',
            'expected_donors',
            'status',
            'stock_updated_after_camp',
            'dashboard_frozen',
            'organizer_name',
            'enrolled_count',
            'created_at'
        ]
        read_only_fields = [
            'organizer_name',
            'enrolled_count',
            'status',
            'stock_updated_after_camp',
            'dashboard_frozen',
            'created_at',
            'city',
            'latitude', 'longitude',
        ]

    def get_enrolled_count(self, obj):
        return obj.enrollments.count()


class CampEnrollmentSerializer(serializers.ModelSerializer):
    camp_title = serializers.CharField(
        source='camp.title',
        read_only=True
    )
    camp_date = serializers.DateField(
        source='camp.camp_date',
        read_only=True
    )

    class Meta:
        model = CampEnrollment
        fields = [
            'id', 'camp', 'camp_title',
            'camp_date', 'name',
            'phone', 'blood_group',
            'attended', 'enrolled_at'
        ]
        read_only_fields = ['attended', 'enrolled_at']