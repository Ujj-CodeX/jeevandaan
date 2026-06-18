from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import jwt
import os

from .models import RefreshToken
from .helpers import generate_jwt_token


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Step 1: decode + validate signature/expiry
        try:
            payload = jwt.decode(refresh_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Refresh token expired. Please login again.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return Response(
                {'error': 'Invalid refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token_id = payload.get('jti')
        user_id = payload.get('id')
        user_type = payload.get('type')

        # ── Step 2: OLD-FORMAT TOKEN (issued before rotation existed, no jti)
        # Production mein already-active users ke paas yeh honge.
        # Inko block nahi karna — naya token issue karke migrate kar do silently.
        if not token_id:
            new_tokens = generate_jwt_token(user_id, user_type)
            return Response(new_tokens)

        # ── Step 3: lookup tracked token in DB
        try:
            stored = RefreshToken.objects.get(token_id=token_id)
        except RefreshToken.DoesNotExist:
            return Response(
                {'error': 'Unknown refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ── Step 4: REUSE DETECTION
        # Already-revoked token dobara use hua = ya replay attack, ya
        # token theft. Safe side — saari sessions revoke karo isi user ki.
        if stored.is_revoked:
            RefreshToken.objects.filter(
                user_id=stored.user_id,
                user_type=stored.user_type,
                is_revoked=False
            ).update(is_revoked=True)

            return Response(
                {'error': 'Token reuse detected. All sessions revoked — please login again.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # ── Step 5: ROTATE — purana revoke, naya issue
        stored.is_revoked = True

        new_tokens = generate_jwt_token(user_id, user_type)
        new_refresh_payload = jwt.decode(new_tokens['refresh'], os.getenv('SECRET_KEY'), algorithms=['HS256'])
        stored.replaced_by = new_refresh_payload['jti']
        stored.save()

        return Response(new_tokens)