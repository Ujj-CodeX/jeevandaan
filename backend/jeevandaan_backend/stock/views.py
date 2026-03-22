from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Stock
from .serializers import StockSerializer
import jwt
import os


# ── Partner updates their stock ───────────────────────
class StockUpdateView(APIView):

    def post(self, request):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            if payload.get('type') != 'partner':
                return Response(
                    {'error': 'Only partners can update stock.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            partner_id = payload['id']
            blood_group = request.data.get('blood_group')
            quantity = request.data.get('quantity')

            if not blood_group or quantity is None:
                return Response(
                    {'error': 'blood_group and quantity are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update if exists, create if not
            stock, created = Stock.objects.update_or_create(
                partner_id=partner_id,
                blood_group=blood_group,
                defaults={'quantity': quantity}
            )

            return Response({
                'message': 'Stock updated successfully.',
                'stock': StockSerializer(stock).data
            })

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


# ── View stock of a specific partner ─────────────────
class PartnerStockView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, partner_id):
        stock = Stock.objects.filter(partner_id=partner_id)
        return Response(StockSerializer(stock, many=True).data)


# ── View critically low stock ─────────────────────────
class CriticalStockView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # quantity less than 3 units = critical
        critical = Stock.objects.filter(quantity__lte=3)
        return Response(StockSerializer(critical, many=True).data)


# ── Search stock by blood group ───────────────────────
class StockSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        blood_group = request.query_params.get('blood_group')
        city = request.query_params.get('city')

        if not blood_group:
            return Response(
                {'error': 'blood_group is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stock = Stock.objects.filter(
            blood_group=blood_group,
            quantity__gt=0,              
            partner__is_live=True,
            partner__is_verified=True,
        )

        if city:
            stock = stock.filter(partner__city__icontains=city)

        return Response(StockSerializer(stock, many=True).data)