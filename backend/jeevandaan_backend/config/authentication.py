import jwt
import os
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv

load_dotenv()


class DonorJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.replace('Bearer ', '').strip()

        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )

            if payload.get('type') != 'donor':
                return None   # ← return None not raise error

            #  Lazy import — avoids circular import
            from users.models import Donor

            donor = Donor.objects.get(id=payload['id'])
            return (donor, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except Exception:
            # ← Catch ALL — never let authenticate() hang
            return None


class PartnerJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.replace('Bearer ', '').strip()

        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )

            if payload.get('type') != 'partner':
                return None   # ← return None not raise error

            #  Lazy import
            from partners.models import Partners

            partner = Partners.objects.get(id=payload['id'])
            return (partner, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except Exception:
            return None


class AnyJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.replace('Bearer ', '').strip()

        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )

            user_type = payload.get('type')

            #  Lazy imports
            if user_type == 'donor':
                from users.models import Donor
                user = Donor.objects.get(id=payload['id'])
            elif user_type == 'partner':
                from partners.models import Partners
                user = Partners.objects.get(id=payload['id'])
            else:
                return None

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except Exception:
            return None