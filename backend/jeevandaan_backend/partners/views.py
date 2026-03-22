from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Partners
from .serializers import (
    PartnerRegisterSerializer,
    PartnerLoginSerializer,
    PartnerProfileSerializer,
    PartnerPublicSerializer
)
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

#--token_generation----------------------


def generate_partner_toekn(partner_id):
    access_payload = {
        'id': partner_id,
        'type': 'partner',
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),

    }
    refresh_payload = {
        'id': partner_id,
        'type': 'partner',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow(),
    }
    access = jwt.encode(access_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    refresh = jwt.encode(refresh_payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return {'access': access, 'refresh': refresh}



#------Register---------------------------------

class PartnerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer_class = PartnerRegisterSerializer(data=request.data)
        if serializer_class.is_valid():
            partner = serializer_class.save()
            tokens = generate_partner_toekn(partner.id)
            return Response({
                'message': 'Partner registered successfully.',
                'tokens': tokens,
                'partner': PartnerProfileSerializer(partner).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


#--------Login ---------------------------------

class PartnerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PartnerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email= serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            partner = Partners.object.get(email=email)
        except Partners.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED

            )
        if not bcrypt.checkpw(password.encode('utf-8'), partner.password.encode('utf-8')):
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not partner.is_live:
            return Response(
                {'error': 'Your account is not live yet. Please wait for approval.'},
                status=status.HTTP_403_FORBIDDEN
            )
        tokens = generate_partner_toekn(partner.id)
        return Response({
            'message': 'Login successful.',
            'tokens': tokens,
            'partner': PartnerProfileSerializer(partner).data
        })
    

class PartnerProfileView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if payload.get('type') != 'partner':
                return Response({'error': 'Invalid token type.'}, status=status.HTTP_401_UNAUTHORIZED)
            partner = Partners.objects.get(id=payload['id'])
            return Response(PartnerProfileSerializer(partner).data)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class PartnerPublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city')
        partner_type = request.query_params.get('type')

        partners = Partners.objects.filter(is_live=True , is_verified=True)
        if city:
            partners = partners.filter(city=city)
        if partner_type:
            partners = partners.filter(type=partner_type)
        serializer = PartnerPublicSerializer(partners, many=True)

        return Response(serializer.data)
    
    
    