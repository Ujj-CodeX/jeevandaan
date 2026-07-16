from flask.cli import load_dotenv

# ── Partner updates their stock ───────────────────────
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Stock, StockUpdateLog
from .serializers import StockSerializer
import jwt
import os
from config.authentication import PartnerJWTAuthentication
from config.permissions import IsPartner

load_dotenv()


class StockUpdateView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        partner = request.user
        try:
           

            partner_id = partner.id
            blood_group = request.data.get('blood_group')
            quantity = request.data.get('quantity')

            if not blood_group or quantity is None:
                return Response(
                    {'error': 'blood_group and quantity are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            valid_groups = [choice[0] for choice in Stock.BLOOD_GROUPS]
            if blood_group not in valid_groups:
                return Response(
                    {'error': f'Invalid blood_group. Must be one of {valid_groups}.'},
                    status=status.HTTP_400_BAD_REQUEST
                    
                )
            try:
                quantity = int(quantity)
            except (TypeError, ValueError):
                return Response(
                    {'error': 'quantity must be a valid integer.'},
                    status=status.HTTP_400_BAD_REQUEST

                )
            if quantity < 0:
                return Response(
                    {'error': 'quantity cannot be negative.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            stock, created = Stock.objects.update_or_create(
                partner_id=partner_id,
                blood_group=blood_group,
                defaults={'quantity': quantity}
            )

            StockUpdateLog.objects.create(
                partner=partner,
                blood_group=blood_group,
                quantity=quantity
            )



            return Response({
                'message': 'Stock updated successfully.',
                'stock': StockSerializer(stock).data
            })

        
        except Exception as e:
            print("ERROR:", str(e))
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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