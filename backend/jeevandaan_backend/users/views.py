from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Donor
from .serializers import DonorRegisterSerializer, DonorLoginSerializer, DonorProfileSerializer
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny
from dotenv import load_dotenv
from .google_auth import verify_google_token

#helper function to generate JWT token
load_dotenv()  
def generate_jwt_token(donor_id):
    access_payload = {
        'id': donor_id,
        'type': 'donor',
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
    }
    refresh_payload = {
        'id': donor_id,
        'type': 'donor',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }

    access =  jwt.encode(access_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    refresh = jwt.encode(refresh_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return {'access': access, 'refresh': refresh}

#register--------------------------------------------------------------------

class DonorRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = DonorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            donor = serializer.save()
            tokens = generate_jwt_token(donor.id)
            return Response({'message': 'Registration successful', 'tokens': tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#LOgin-----------------------------------------------------------------------
class DonorLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DonorLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                donor = Donor.objects.get(username=username)
            except Donor.DoesNotExist:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

            if not bcrypt.checkpw(password.encode(), donor.password.encode()):
                return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

            if donor.is_locked:
                return Response(
                {'error': 'Account locked. Please try again later.'},
                status=status.HTTP_403_FORBIDDEN
            )
            print("SIGN KEY:", os.getenv('SECRET_KEY'))

            tokens = generate_jwt_token(donor.id)
            return Response({
            'message': 'Login successful.',
            'tokens': tokens,
            'donor': DonorProfileSerializer(donor).data
        })

class DonorProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        print("AUTH HEADER:", auth_header)

        if not auth_header:
            return Response(
                {'error': 'No token provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.replace('Bearer ', '').strip()  # ← defined before try block
        print("TOKEN:", token)
        print("VERIFY KEY:", os.getenv('SECRET_KEY'))

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            print("PAYLOAD:", payload)
            donor = Donor.objects.get(id=payload['id'])
            return Response(DonorProfileSerializer(donor).data)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            print("JWT ERROR:", str(e))
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Donor.DoesNotExist:
            return Response({'error': 'Donor not found.'}, status=status.HTTP_404_NOT_FOUND)
        



class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response(
                {'error': 'Google token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token with Google
        user_info = verify_google_token(token)

        if not user_info:
            return Response(
                {'error': 'Invalid Google token.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        email = user_info['email']
        google_id = user_info['google_id']
        name = user_info['name']

        # Check if donor already exists
        donor = Donor.objects.filter(email=email).first()

        if donor:
            # Existing donor — just login
            # Update google_id if not set
            if not donor.google_id:
                donor.google_id = google_id
                donor.auth_provider = 'google'
                donor.save()

            tokens = generate_jwt_token(donor.id)
            return Response({
                'message': 'Login successful.',
                'tokens': tokens,
                'donor': DonorProfileSerializer(donor).data,
                'is_new_user': False
            })

        else:
            # New donor — create account
            # Auto generate username from email
            username = email.split('@')[0]

            # Make username unique if taken
            if Donor.objects.filter(username=username).exists():
                username = f"{username}_{google_id[:6]}"

            donor = Donor.objects.create(
                name=name,
                email=email,
                username=username,
                google_id=google_id,
                auth_provider='google',
                password=None,          # no password for Google users
                blood_group=None,       # will be filled in profile completion
            )

            tokens = generate_jwt_token(donor.id)
            return Response({
                'message': 'Account created successfully.',
                'tokens': tokens,
                'donor': DonorProfileSerializer(donor).data,
                'is_new_user': True,    # ← Vue.js redirects to complete profile
            }, status=status.HTTP_201_CREATED)