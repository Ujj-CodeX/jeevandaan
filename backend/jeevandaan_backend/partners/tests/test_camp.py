
from flask import json
import pytest
import jwt
import os
import bcrypt
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.test import APIClient
from users.models import Donor
from partners.models import Partners, DonationCamp
from requests_app.models import PartnerDonorRequest, OTPCode
from chat.models import Chat

pytest.mark.django_db
class TestCampScheduling:
 
    def test_partner_can_create_camp(self, auth_partner_client, partner):
        """Partner can create a donation camp"""
        response = auth_partner_client.post('/api/partners/camps/create/', {
            'title': 'Blood Donation Camp',
            'description': 'Test camp',
            'location': 'Delhi Community Hall',
            'camp_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'blood_groups_needed': json.dumps(['A+', 'O+', 'B+']),
            'expected_donors': 50,
        })
        print(response.data)  # ← yeh add karo
    
        assert response.status_code == 201
        assert DonationCamp.objects.filter(organizer=partner).exists()
        
 
    def test_donor_can_enroll_in_camp(self, auth_donor_client, donor, partner):
        """Donor can enroll in a scheduled camp"""
        camp = DonationCamp.objects.create(
            organizer=partner,
            title='Test Camp',
            location='Delhi',
            city='Delhi',
            camp_date=(datetime.now() + timedelta(days=5)).date(),
            start_time='09:00:00',
            end_time='17:00:00',
            status='scheduled',
            latitude=28.6139,
            longitude=77.2090,
        )
        response = auth_donor_client.post(f'/api/partners/camps/{camp.id}/enroll/', {
            'name': donor.name,
            'phone': donor.phone_number,
            'blood_group': donor.blood_group,
        })
        assert response.status_code == 201
 
    def test_donor_cannot_enroll_twice(self, auth_donor_client, donor, partner):
        """Duplicate enrollment must be blocked"""
        camp = DonationCamp.objects.create(
            organizer=partner,
            title='Test Camp',
            location='Delhi',
            city='Delhi',
            camp_date=(datetime.now() + timedelta(days=5)).date(),
            start_time='09:00:00',
            end_time='17:00:00',
            status='scheduled',
            latitude=28.6139,
            longitude=77.2090,
        )
        # First enrollment
        auth_donor_client.post(f'/api/partners/camps/{camp.id}/enroll/', {
            'name': donor.name,
            'phone': donor.phone_number,
            'blood_group': donor.blood_group,
        })
        # Second enrollment — must fail
        response = auth_donor_client.post(f'/api/partners/camps/{camp.id}/enroll/', {
            'name': donor.name,
            'phone': donor.phone_number,
            'blood_group': donor.blood_group,
        })
        assert response.status_code == 400
 
    def test_past_camp_enrollment_blocked(self, auth_donor_client, donor, partner):
        """Cannot enroll in a camp that already passed"""
        camp = DonationCamp.objects.create(
            organizer=partner,
            title='Old Camp',
            location='Delhi',
            city='Delhi',
            camp_date=(datetime.now() - timedelta(days=1)).date(),  # yesterday
            start_time='09:00:00',
            end_time='17:00:00',
            status='scheduled',
            latitude=28.6139,
            longitude=77.2090,
        )
        response = auth_donor_client.post(f'/api/partners/camps/{camp.id}/enroll/', {
            'name': donor.name,
            'phone': donor.phone_number,
            'blood_group': donor.blood_group,
        })
        assert response.status_code == 400
 
    def test_camp_stock_update_marks_completed(self, auth_partner_client, partner):
        """After camp, marking stock updated should set status to completed"""
        camp = DonationCamp.objects.create(
            organizer=partner,
            title='Done Camp',
            location='Delhi',
            city='Delhi',
            camp_date=datetime.now().date(),
            start_time='09:00:00',
            end_time='17:00:00',
            status='scheduled',
            latitude=28.6139,
            longitude=77.2090,
        )
        response = auth_partner_client.post(
            f'/api/partners/camps/{camp.id}/update-stock/'
        )
        assert response.status_code == 200
        camp.refresh_from_db()
        assert camp.status == 'completed'
        assert camp.stock_updated_after_camp == True
 
    def test_download_available_only_on_camp_date(self, auth_partner_client, partner):
        """CSV download must be blocked before camp date"""
        camp = DonationCamp.objects.create(
            organizer=partner,
            title='Future Camp',
            location='Delhi',
            city='Delhi',
            camp_date=(datetime.now() + timedelta(days=10)).date(),  # future
            start_time='09:00:00',
            end_time='17:00:00',
            status='scheduled',
            latitude=28.6139,
            longitude=77.2090,
        )
        response = auth_partner_client.get(
            f'/api/partners/camps/{camp.id}/download/'
        )
        assert response.status_code == 403
 