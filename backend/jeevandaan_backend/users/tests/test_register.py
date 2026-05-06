import pytest

@pytest.mark.django_db
class TestDonorRegister:
    def test_donor_registration(self, api_client,donor_payload):
        response = api_client.post('/api/users/register/', donor_payload)

        assert response.status_code == 201
        assert response.data['message'] == "Registration successful"

    def test_donor_registration_with_existing_email(self, api_client, donor_payload, donor):
        # Attempt to register with the same email as the existing donor
        response = api_client.post('/api/users/register/', donor_payload)

        assert response.status_code == 400
    def test_duplicate_email(self , api_client, donor, donor_payload):
        donor_payload['username']="diff_username"

        response = api_client.post('/api/users/register/', donor_payload)
        assert response.status_code == 400
    def test_missing_fields(self, api_client,donor_payload):
        donor_payload.pop('password')
        response = api_client.post('/api/users/register/', donor_payload)
        assert response.status_code == 400

    def test_missing_email(self, api_client, donor_payload):
        donor_payload.pop('email')
        response = api_client.post('/api/users/register/', donor_payload)
        assert response.status_code == 400
    
    def test_invalid_blood_group(self, api_client, donor_payload):
        donor_payload['blood_group'] = 'XYZ'  # invalid value

        response = api_client.post('/api/users/register/', donor_payload)

        assert response.status_code == 400

    def text_duplicate_username(self, api_client, donor, donor_payload):
        response = api_client.post('/api/users/register/', donor_payload)
        assert response.status_code == 400

    