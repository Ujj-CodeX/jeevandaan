from flask.cli import load_dotenv
from django.db.models import Q
from geopy.distance import geodesic
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





# ── Search stock by blood group ───────────────────────
#############################
# Warning: This Viewned point is not wired in frontend yet or nay vue. Exist there for future usecase. 
#############################
class StockSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        blood_group = request.query_params.get('blood_group')
        city = request.query_params.get('city')
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

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
        ).select_related('partner')   # ← fix 2: N+1 avoid — 1 JOIN query instead of N

        if city:
            stock = stock.filter(partner__city__icontains=city)

        # ── fix 1: distance sort — only when lat/lng given ──
        if lat and lng:
            try:
                lat, lng = float(lat), float(lng)
            except (TypeError, ValueError):
                return Response(
                    {'error': 'lat and lng must be valid numbers.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with_location = stock.filter(
                partner__latitude__isnull=False,
                partner__longitude__isnull=False,
            )
            without_location = stock.filter(
                Q(partner__latitude__isnull=True) | Q(partner__longitude__isnull=True)
            )

            results = []
            for s in with_location:
                distance = geodesic(
                    (lat, lng),
                    (float(s.partner.latitude), float(s.partner.longitude))
                ).km
                data = StockSerializer(s).data
                data['distance_km'] = round(distance, 1)
                results.append(data)

            results.sort(key=lambda x: x['distance_km'])

            # location-missing partners — end mein, distance unknown
            for s in without_location:
                data = StockSerializer(s).data
                data['distance_km'] = None
                results.append(data)

            return Response(results)

        return Response(StockSerializer(stock, many=True).data)