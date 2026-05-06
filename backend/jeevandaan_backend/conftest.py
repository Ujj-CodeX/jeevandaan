import pytest
from rest_framework.test import APIClient
from users.models import Donor
from partners.models import Partners
import bcrypt


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def donor(db):
    return Donor.objects.create(
        name="Test Donor",
        username="test_donor",
        blood_group="A+",
        google_id="test_google_id",
        auth_provider="local",
        email="donor@test.com",
        phone_number="1234567890",
        password=bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        is_aadhaar_verified=True,
        aadhaar_number="123456789012",
        reliability_score=4.5,
        total_donations=5,
        member_tag="Gold Member",
        cancellation_count=1,
        is_locked=False,
        locked_until=None,
        total_requests_raised=3,
        latitude=12.9716,
        longitude=77.5946,
    )


@pytest.fixture
def partner(db):
    return Partners.objects.create(
        hospital_name="Test Partner",
        license_id="LIC123",
        email="testpartner@gmail.com",
        contact="1234567890",
        password=bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        is_live=True,
        is_verified=True,
        latitude=28.6139,
        longitude=77.2090,
        city="Delhi",
        state="Delhi",
        address="123 Test Street, Delhi",
        partner_type="government",
        facility="24*7",
        convenience_fee=1200,
    )


@pytest.fixture
def donor_payload():
    return {
        'name': 'Test Donor',
        'username': 'test_donor',
        'email': 'donor@test.com',
        'phone_number': '1234567890',
        'password': 'password',
        'blood_group': 'A+',
    }


@pytest.fixture
def donor_token(donor):
    import jwt
    import os
    from datetime import datetime, timedelta
    payload = {
        'id': donor.id,
        'type': 'donor',
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, os.getenv('SECRET_KEY', 'testsecret'), algorithm='HS256')


@pytest.fixture
def partner_token(partner):
    import jwt
    import os
    from datetime import datetime, timedelta
    payload = {
        'id': partner.id,
        'type': 'partner',
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, os.getenv('SECRET_KEY', 'testsecret'), algorithm='HS256')


@pytest.fixture
def auth_donor_client(api_client, donor_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {donor_token}')
    return api_client


@pytest.fixture
def auth_partner_client(api_client, partner_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {partner_token}')
    return api_client

