
import uuid
from datetime import datetime, timedelta
from auth_token.models import RefreshToken
import jwt,os

def generate_jwt_token(user_id, user_type='donor'):
    token_id = uuid.uuid4()

    access_payload = {
        'id': user_id, 'type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
    }
    refresh_payload = {
        'id': user_id, 'type': user_type,
        'jti': str(token_id),   # ← unique identifier, rotation ke liye zaruri
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }

    RefreshToken.objects.create(
        token_id=token_id,
        user_type=user_type,
        user_id=user_id,
        expires_at=refresh_payload['exp']
    )

    access = jwt.encode(access_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    refresh = jwt.encode(refresh_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return {'access': access, 'refresh': refresh}