from urllib import response
from rest_framework.test import APIClient
from datetime import datetime, timedelta
import pytest
import jwt, os, bcrypt

import pytest

@pytest.mark.django_db

class TestDonorlogin:
    def test_successful_login(self,api_client,donor):
        response = api_client.post('/api/users/login/',{
            'username' :'test_donor',
            'password' :'password',
        })
        assert response.status_code == 200
        assert 'access' in response.data['tokens']

    def test_wrong_password(self, api_client, donor):
        response = api_client.post('/api/users/login/',{
            'username': 'test_donor',
            'password': 'wrongpassword',

        })
        assert response.status_code == 401
    
    def test_locked_account(self, api_client, donor):
        donor.is_locked = True
        donor.save()

        response = api_client.post('/api/users/login/',{
            'username': 'test_donor',
            'password': 'password',
        })
        assert response.status_code == 403

    def test_aadhaar_submission(self,auth_donor_client,donor):
        donor.is_aadhaar_verified = False
        donor.aadhaar_no = None
        donor.save()

        response = auth_donor_client.post('/api/users/verify-aadhaar/',{
                'aadhaar_no': '123456789012',   })
            
        assert response.status_code == 200

        donor.refresh_from_db()
        assert donor.is_aadhaar_verified == False

    def test_aadhaar_verified_blocked(self,auth_donor_client,donor):
        
        response = auth_donor_client.post('/api/users/verify-aadhaar/',{
                'aadhaar_number': '123456789012',   })
            
        assert response.status_code == 400

    
class TestRaceConditon:
    def test_same_request_cannot_be_accepted_twice(self, donor, partner):

        from requests_app.models import PartnerDonorRequest
        from django.utils import timezone
        from datetime import timedelta
        from users.models import Donor

        import jwt, os , bcrypt

        donor2 = Donor.objects.create(
            name ="Donor2" , username="donor2" , email="donor@gmail.com",
            blood_group="A+", is_aadhaar_verified=True,
            aadhaar_number="999988887777",
            password=bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode()
        
        )
        req = PartnerDonorRequest.objects.create(
            partner=partner, blood_group='A+', quantity=1,
            status='open',
            expires_at=timezone.now() + timedelta(hours=12)
        )

        client1= APIClient()

        token1 = jwt.encode(
            {'id': donor.id, 'type': 'donor',
             'exp': datetime.utcnow() + timedelta(hours=1)},
            os.getenv('SECRET_KEY', 'testsecret'), algorithm='HS256'
        )
        client1.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        token1 = jwt.encode(
            {'id': donor.id, 'type': 'donor',
             'exp': datetime.utcnow() + timedelta(hours=1)},
            os.getenv('SECRET_KEY', 'testsecret'), algorithm='HS256'
        )
        client1.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        response1 = client1.post(f'/api/requests/donor/{req.id}/accept/') 

        assert response1.status_code==200

        client2 = APIClient()

        token2 = jwt.encode(
            {'id': donor2.id, 'type': 'donor',
             'exp': datetime.utcnow() + timedelta(hours=1)},
            os.getenv('SECRET_KEY', 'testsecret'), algorithm='HS256'
        )
        client2.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')

        response2 = client2.post(f'/api/requests/donor/{req.id}/accept/')
        assert response2.status_code == 404  # Already assigned — not found

