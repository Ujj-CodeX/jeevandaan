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
from dotenv import load_dotenv
from users.location import get_nearby_partners, get_nearby_donors
from stock.models import Stock



#--token_generation----------------------
load_dotenv() 


def generate_partner_token(partner_id):
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



class NearbyPartnersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        blood_group = request.query_params.get('blood_group')
        radius = request.query_params.get('radius', 10)

        if not lat or not lng:
            return Response(
                {'error': 'lat and lng are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        partners = Partners.objects.filter(
            is_live=True,
            is_verified=True
        )

        if blood_group:
            partners = partners.filter(
                stock__blood_group=blood_group,
                stock__quantity__gt=0
            )

        nearby = get_nearby_partners(lat, lng, partners, float(radius))

        result = []
        for item in nearby:
            partner_data = PartnerPublicSerializer(item['partner']).data
            partner_data['distance_km'] = item['distance_km']

            if blood_group:
                stock = Stock.objects.filter(
                    partner=item['partner'],
                    blood_group=blood_group
                ).first()
                partner_data['available_units'] = stock.quantity if stock else 0

            result.append(partner_data)

        return Response(result)


class NearbyDonorsView(APIView):

    def get(self, request):
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can search donors.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            lat = request.query_params.get('lat')
            lng = request.query_params.get('lng')
            blood_group = request.query_params.get('blood_group')
            radius = request.query_params.get('radius', 10)

            if not lat or not lng or not blood_group:
                return Response(
                    {'error': 'lat, lng and blood_group are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            from users.models import Donor
            donors = Donor.objects.filter(
                blood_group=blood_group,
                is_locked=False,
                is_aadhaar_verified=True
            )

            nearby = get_nearby_donors(lat, lng, donors, float(radius))

            result = []
            for item in nearby:
                result.append({
                    'blood_group': item['donor'].blood_group,
                    'member_tag': item['donor'].member_tag,
                    'reliability_score': item['donor'].reliability_score,
                    'distance_km': item['distance_km'],
                })

            return Response(result)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

#------Register---------------------------------

class PartnerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer_class = PartnerRegisterSerializer(data=request.data)
        if serializer_class.is_valid():
            partner = serializer_class.save()
            tokens = generate_partner_token(partner.id)
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
            partner = Partners.objects.get(email=email)
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
        tokens = generate_partner_token(partner.id)
        return Response({
            'message': 'Login successful.',
            'tokens': tokens,
            'partner': PartnerProfileSerializer(partner).data
        })
    

class PartnerProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        print("AUTH HEADER:", auth_header)

        token = auth_header.replace('Bearer ', '').strip()
        print("TOKEN:", token)
        print("SECRET:", os.getenv('SECRET_KEY'))

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            print("PAYLOAD:", payload)

            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Invalid token type.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            partner = Partners.objects.get(id=payload['id'])
            return Response(PartnerProfileSerializer(partner).data)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            print("JWT ERROR:", str(e))
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Partners.DoesNotExist:
            return Response({'error': 'Partner not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class PartnerPublicListView(APIView):
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
    
    
    