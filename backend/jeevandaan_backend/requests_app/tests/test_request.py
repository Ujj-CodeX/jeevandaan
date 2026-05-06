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


@pytest.mark.django_db
class Testchatsending:
    def test_donor_can_send_valid_message(self, auth_donor_client,donor, partner):
        req = PartnerDonorRequest.objects.create(partner=partner, assigned_donor=donor, blood_group ='A+' ,quantity=1,status='assigned',expires_at=timezone.now() + timedelta(hours=12))
        response = auth_donor_client.post(f'/api/chat/{req.id}/send/', {'message': 'on_the_way'})
        assert response.status_code == 201

        assert Chat.objects.filter(request=req, sender_type='donor', message='on_the_way').exists()
        
    def test_partner_can_send_valid_message(self, auth_partner_client, partner, donor):
        req = PartnerDonorRequest.objects.create(partner=partner, assigned_donor=donor, blood_group ='A+' ,quantity=1,status='assigned',expires_at=timezone.now() + timedelta(hours=12))
        response = auth_partner_client.post(f'/api/chat/{req.id}/send/', {'message': 'donation_received'})
        assert response.status_code == 201

        
    def test_unassigned_donor_cannot_send(self , donor , partner):
        other_donor = Donor.objects.create(name="Other Donor", username="other_donor", blood_group="A+", is_aadhaar_verified=True,aadhaar_number="111111111111",email="other@test.com",password=bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode()                 )
        req = PartnerDonorRequest.objects.create(
            partner=partner,
            assigned_donor=donor,
            blood_group='A+',
            quantity=1,
            status='assigned',
            expires_at=timezone.now() + timedelta(hours=12)

        )        
        client = APIClient()
        token = jwt.encode(
            {'id': other_donor.id, 'type': 'donor',
             'exp': datetime.utcnow() + timedelta(hours=1)},
            os.getenv('SECRET_KEY', 'testsecret'), algorithm='HS256'
        )
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = client.post(f'/api/chat/{req.id}/send/', {'message': 'on_the_way'})
        assert response.status_code == 403

    def test_chat_closed_after_fulfillment(self, auth_donor_client, donor, partner):
        """No messages allowed after request is fulfilled"""
        req = PartnerDonorRequest.objects.create(
            partner=partner,
            assigned_donor=donor,
            blood_group='A+',
            quantity=1,
            status='fulfilled',  # already done
            expires_at=timezone.now() + timedelta(hours=12)
        )
        response = auth_donor_client.post(f'/api/chat/{req.id}/send/', {
            'message': 'on_the_way'
        })
        assert response.status_code == 400
    
    def test_chat_history_returns_all_messages(self, auth_donor_client, donor, partner):
        """Chat history must return messages in order"""
        req = PartnerDonorRequest.objects.create(
            partner=partner,
            assigned_donor=donor,
            blood_group='A+',
            quantity=1,
            status='assigned',
            expires_at=timezone.now() + timedelta(hours=12)
        )
        Chat.objects.create(request=req, sender_type='donor', message='on_the_way')
        Chat.objects.create(request=req, sender_type='donor', message='reached')
 
        response = auth_donor_client.get(f'/api/chat/{req.id}/history/')
        assert response.status_code == 200
        assert len(response.data) == 2

    
      
