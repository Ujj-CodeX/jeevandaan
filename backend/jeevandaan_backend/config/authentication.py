import jwt
import os
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed     
from users.models import Donor
from partners.models import Partner
from dotenv import load_dotenv

load_dotenv()


class DonorJWTAuthentication(BaseAuthentication):
    """
    Custom JWT auth for Donors
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if payload.get('user_type') != 'donor':
                raise AuthenticationFailed('Invalid token for donor')
            donor = Donor.objects.get(id=payload['id'])
            return (donor, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except Donor.DoesNotExist:
            raise AuthenticationFailed('Donor not found.')
        

class PartnerJWTAuthentication(BaseAuthentication):
    """
    Custom JWT auth for Partners
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if payload.get('type') != 'partner':
                raise AuthenticationFailed('Invalid token for partner')
            partner = Partner.objects.get(id=payload['id'])
            return (partner, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except Partner.DoesNotExist:
            raise AuthenticationFailed('Partner not found.')
        
class AnyJWTAuthentication(BaseAuthentication):
    """
    Accepts both Donor and Partner tokens,
    Use for shared endpoint like chat
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header.startswith('Bearer '):
            return None
        token = auth_header.replace('Bearer ', '').strip()
        
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user_type = payload.get('type')
            if user_type == 'donor':
                user = Donor.objects.get(id=payload['id'])
            elif user_type == 'partner':
                user = Partner.objects.get(id=payload['id'])
            else:
                raise AuthenticationFailed('Invalid token for any user type')
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except (Donor.DoesNotExist, Partner.DoesNotExist):
            raise AuthenticationFailed('User not found.')