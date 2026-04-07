import jwt
import os
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from partners.models import Partners  # confirm model name

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')

        if not header:
            return None

        try:
            token = header.split(' ')[1]
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            partner = Partners.objects.get(id=payload['id'])
        except Exception:
            raise AuthenticationFailed('Invalid or expired token')

        return (partner, None)