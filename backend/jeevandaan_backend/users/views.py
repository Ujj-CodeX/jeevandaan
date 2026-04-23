from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Donor
from .serializers import DonorRegisterSerializer, DonorLoginSerializer, DonorProfileSerializer
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from dotenv import load_dotenv
from config.authentication import DonorJWTAuthentication
from config.permissions import IsDonor

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
    authentication_classes = []
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
    authentication_classes = []
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
            
            tokens = generate_jwt_token(donor.id)
            return Response({
            'message': 'Login successful.',
            'tokens': tokens,
            'donor': DonorProfileSerializer(donor).data
        })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DonorProfileView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def get(self, request):
        donor = request.user
        return Response(DonorProfileSerializer(donor).data)
        
        
        





class UpdateDonorLocationView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request):
        try:
            
            donor = request.user

            lat = request.data.get('latitude')
            lng = request.data.get('longitude')

            if not lat or not lng:
                return Response(
                    {'error': 'latitude and longitude required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            donor.latitude = lat
            donor.longitude = lng
            donor.save()

            return Response({'message': 'Location updated '})

        
        except Donor.DoesNotExist:
            return Response({'error': 'Donor not found.'}, status=status.HTTP_404_NOT_FOUND)


import random

class ForgotPasswordView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                {'error': 'Email is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            donor = Donor.objects.get(email=email)

            # Generate 6 digit OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Store in cache or temp model
            
            from django.core.cache import cache
            cache.set(f'reset_otp_{email}', otp, timeout=600)  # 10 mins

            # Send via SMS
            from notifications.helpers import notify_donor
            notify_donor(
                donor=donor,
                trigger='account_locked',
                message=f'JeevanDaan+ Password Reset OTP: {otp}. Valid for 10 minutes.'
            )

            return Response({
                'message': 'OTP sent to your registered phone number.'
            })

        except Donor.DoesNotExist:
            return Response(
                {'error': 'No account found with this email.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ResetPasswordView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not all([email, otp, new_password]):
            return Response(
                {'error': 'Email, OTP and new password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.core.cache import cache
        stored_otp = cache.get(f'reset_otp_{email}')

        if not stored_otp or stored_otp != otp:
            return Response(
                {'error': 'Invalid or expired OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            donor = Donor.objects.get(email=email)

            # Validate new password
            if len(new_password) < 8:
                return Response(
                    {'error': 'Password must be at least 8 characters.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Hash and save
            import bcrypt
            donor.password = bcrypt.hashpw(
                new_password.encode(),
                bcrypt.gensalt()
            ).decode()
            donor.save()

            # Clear OTP
            cache.delete(f'reset_otp_{email}')

            return Response({
                'message': 'Password reset successfully!  '
            })

        except Donor.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ChangePasswordView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request):
        
            
            donor = request.user

            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')

            if not all([current_password, new_password]):
                return Response(
                    {'error': 'Both passwords required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify current password
            import bcrypt
            if not bcrypt.checkpw(
                current_password.encode(),
                donor.password.encode()
            ):
                return Response(
                    {'error': 'Current password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(new_password) < 8:
                return Response(
                    {'error': 'New password must be at least 8 characters.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            donor.password = bcrypt.hashpw(
                new_password.encode(),
                bcrypt.gensalt()
            ).decode()
            donor.save()

            return Response({
                'message': 'Password changed successfully! '
            })

        

class VerifyAadhaarView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request):
        try:
        
           
            donor = request.user

            aadhaar_no = request.data.get('aadhaar_no')

            
            if not aadhaar_no:
                return Response(
                    {'error': 'Aadhaar number is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            aadhaar_no = str(aadhaar_no).strip()

            if not aadhaar_no.isdigit() or len(aadhaar_no) != 12:
                return Response(
                    {'error': 'Invalid Aadhaar number. Must be 12 digits.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            if donor.is_aadhaar_verified:
                return Response(
                    {'error': 'Aadhaar already verified.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            if Donor.objects.filter(aadhaar_number=aadhaar_no).exclude(id=donor.id).exists():
                return Response(
                    {'error': 'This Aadhaar is already linked with another account.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            donor.aadhaar_number = aadhaar_no
            donor.is_aadhaar_verified = False   
            donor.save()

            return Response({
                'message': 'Aadhaar submitted. Verification is pending.'
            })


        except Donor.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class UpdateProfileView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def put(self, request):
        try:
            
            donor = request.user

        
            name = request.data.get('name')
            phone = request.data.get('phone_number')
            blood_group = request.data.get('blood_group')
            address = request.data.get('address')

            
            if not name:
                return Response({'error': 'Name is required.'}, status=400)

            if blood_group not in dict(Donor.BLOOD_GROUPS):
                return Response({'error': 'Invalid blood group.'}, status=400)

            
            donor.name = name
            donor.phone_number = phone
            donor.blood_group = blood_group
            donor.address = address
            donor.save()

    
            return Response({
                'name': donor.name,
                'email': donor.email,
                'phone_number': donor.phone_number,
                'blood_group': donor.blood_group,
                'address': donor.address
            })


        except Donor.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)