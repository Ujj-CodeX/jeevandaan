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

from config.logger import get_logger
logger = get_logger(__name__)

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

            logger.info("donor_registered", extra={"donor_id": donor.id, "blood_group": donor.blood_group})
                  
            return Response({'message': 'Registration successful', 'tokens': tokens}, status=status.HTTP_201_CREATED)
        
        logger.warning("donor_registration_invalid", extra={"errors": serializer.errors})
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
                logger.warning("donor_login_user_not_found")
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

            if not bcrypt.checkpw(password.encode(), donor.password.encode()):

                logger.warning("donor_login_wrong_password", extra={"donor_id": donor.id})

                return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

            if donor.is_locked:
                logger.warning("donor_login_account_locked", extra={"donor_id": donor.id ,"locked_until": str(donor.locked_until)}) 
                return Response(
                {'error': 'Account locked. Please try again later.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
            tokens = generate_jwt_token(donor.id)

            logger.info("donor_login_successful", extra={"donor_id": donor.id})
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

                logger.warning("donor_location_update_missing_coords", extra = {"donor_id": donor.id}  )
                return Response(
                    {'error': 'latitude and longitude required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            donor.latitude = lat
            donor.longitude = lng
            donor.save()

            logger.debug("donor_location_updated", extra={"donor_id": donor.id, "lat": str(lat), "lng": str(lng) })

            return Response({'message': 'Location updated '})

        
        except Donor.DoesNotExist:

            logger.exception("donor_location_updated_failed", extra={"donor_id": donor.id})


            return Response({'error': 'Donor not found.'}, status=status.HTTP_404_NOT_FOUND)


import random

class ForgotPasswordView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        if not email:

            logger.warning("forgot_password_no_email")


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

            logger.info("forgot_password_otp_sent", extra={
                "donor_id": donor.id,
            })



            return Response({
                'message': 'OTP sent to your registered phone number.'
            })

        except Donor.DoesNotExist:

            logger.warning("forgot_password_email_not_found")   


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

            logger.warning("reset_password_missing_fields")
            return Response(
                {'error': 'Email, OTP and new password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.core.cache import cache
        stored_otp = cache.get(f'reset_otp_{email}')

        if not stored_otp or stored_otp != otp:

            logger.warning("reset_password_invalid_otp")
            return Response(
                {'error': 'Invalid or expired OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            donor = Donor.objects.get(email=email)

            # Validate new password
            if len(new_password) < 8:

                logger.warning("reset_password_weak_password", extra={"donor_id": donor.id})
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

            logger.info("reset_password_success", extra={"donor_id": donor.id})

            return Response({
                'message': 'Password reset successfully!  '
            })

        except Donor.DoesNotExist:
            logger.warning("reset_password_donor_not_found", extra={"email": email})
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
                logger.warning("change_password_missing_fields",extra={"donor_id": donor.id})
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
                logger.warning("change_password_wrong_current",extra={"donor_id": donor.id})
                return Response(
                    {'error': 'Current password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(new_password) < 8:
                logger.warning("change_password_weak_new",extra={"donor_id": donor.id})
                return Response(
                    {'error': 'New password must be at least 8 characters.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            donor.password = bcrypt.hashpw(
                new_password.encode(),
                bcrypt.gensalt()
            ).decode()
            donor.save()

            logger.info("change_password_success",extra={"donor_id": donor.id})

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

                logger.warning("aadhaar_submit_missing", extra={"donor_id": donor.id})
                return Response(
                    {'error': 'Aadhaar number is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            aadhaar_no = str(aadhaar_no).strip()

            if not aadhaar_no.isdigit() or len(aadhaar_no) != 12:
                logger.warning("aadhaar_submit_invalid_format", extra={"donor_id": donor.id})
                return Response(
                    {'error': 'Invalid Aadhaar number. Must be 12 digits.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            if donor.is_aadhaar_verified:

                logger.warning("aadhaar_already_verified", extra={"donor_id": donor.id})
                return Response(
                    {'error': 'Aadhaar already verified.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            if Donor.objects.filter(aadhaar_number=aadhaar_no).exclude(id=donor.id).exists():
                logger.warning("aadhaar_duplicate_attempt", extra={"donor_id": donor.id})
                return Response(
                    {'error': 'This Aadhaar is already linked with another account.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            
            donor.aadhaar_number = aadhaar_no
            donor.is_aadhaar_verified = False   
            donor.save()

            logger.info("aadhaar_submitted_pending_verification", extra={
                "donor_id": donor.id,
            })

            return Response({
                'message': 'Aadhaar submitted. Verification is pending.'
            })


        except Donor.DoesNotExist:
            logger.exception("aadhaar_submit_unexpected_error", extra={"donor_id": getattr(request.user, 'id', None)})
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
                logger.warning("update_profile_missing_name", extra={"donor_id": donor.id})
                return Response({'error': 'Name is required.'}, status=400)

            if blood_group not in dict(Donor.BLOOD_GROUPS):
                logger.warning("update_profile_invalid_blood_group", extra={"donor_id": donor.id ,  "blood_group_verified": blood_group,})
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
            logger.exception("profile_update_unexpected_error", extra={"donor_id": getattr(request.user, 'id', None)})


            #actually yaha pe Get attr wala stateement isliye use kr rhen in exception if in case agr donor.id bani he nhi 
            #try block mein crash kr jaye so just to handle exception we gettattr(request.user--> object , attribute --> id , default --> None)
            return Response({'error': 'User not found.'}, status=404)


            