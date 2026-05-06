import pytest
@pytest.mark.django_db
class TestDonorScoreLogic:
    def test_donor_locked_after_3_cancellation(self, auth_donor_client,donor,partner):
        from requests_app.models import PartnerDonorRequest
        from django.utils import timezone
        from datetime import timedelta
 
        donor.cancellation_count = 2
        donor.save()

        req = PartnerDonorRequest.objects.create(partner=partner, assigned_donor=donor, blood_group ='A+' ,quantity=1,status='assigned',expires_at=timezone.now() + timedelta(hours=12))


        response =  auth_donor_client.post(f'/api/requests/donor/{req.id}/cancel/', {'reason': 'Test Cancellation'})  

        assert response.status_code == 200 
        donor.refresh_from_db()
        assert donor.is_locked == True

