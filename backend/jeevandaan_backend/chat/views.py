from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer
from requests_app.models import PartnerDonorRequest
from users.models import Donor
from partners.models import Partners
import jwt
import os


# ── helper ───────────────────────────────────────────
def decode_token(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

#sendmaeesage -----------------

class SendMessageView(APIView):
    def post(self, request, request_id):
        try:
            print("🔴 SEND MESSAGE HIT")  # ← add this first
            payload = decode_token(request)
            print("✅ TOKEN DECODED:", payload)  # ← add this
            
            user_id = payload.get('id')

            if Partners.objects.filter(id=user_id).exists():
                sender_type = 'partner'
            elif Donor.objects.filter(id=user_id).exists():
                sender_type = 'donor'
            else:
                return Response({'error': 'Invalid user'}, status=status.HTTP_403_FORBIDDEN)
            
            print("✅ SENDER TYPE:", sender_type)  # ← add this

            try:
                req = PartnerDonorRequest.objects.get(id=request_id)
                print("✅ REQUEST FOUND:", req.id, "STATUS:", req.status)  # ← add this
            except PartnerDonorRequest.DoesNotExist:
                return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            if req.status in ['fulfilled', 'expired', 'cancelled']:
                print("❌ CHAT CLOSED")  # ← add this
                return Response({'error': 'Chat is closed for this request.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if sender_type == 'donor':
                donor = Donor.objects.get(id=payload['id'])
                print("✅ DONOR:", donor, "ASSIGNED:", req.assigned_donor)  # ← add this
                if req.assigned_donor != donor:
                    print("❌ DONOR NOT ASSIGNED")  # ← add this
                    return Response({'error': 'You are not assigned to this request.'}, status=status.HTTP_403_FORBIDDEN)
            
            elif sender_type == 'partner':
                partner = Partners.objects.get(id=payload['id'])
                print("✅ PARTNER:", partner, "REQ PARTNER:", req.partner)  # ← add this
                if req.partner != partner:
                    print("❌ WRONG PARTNER")  # ← add this
                    return Response({'error': 'This request does not belong to you.'}, status=status.HTTP_403_FORBIDDEN)

            message = request.data.get('message')
            print("✅ MESSAGE:", message)  # ← add this
            
            valid_messages = [
                'on_the_way', 'reached', 'unable_to_come', 'delayed', 'donated',
                'waiting_for_donor', 'donor_arrived', 'please_hurry',
                'donation_received', 'request_cancelled'
            ]
            if message not in valid_messages:
                print("❌ INVALID MESSAGE:", message)  # ← add this
                return Response({'error': 'Invalid message.'}, status=status.HTTP_400_BAD_REQUEST)
            
            chat = Chat.objects.create(request=req, sender_type=sender_type, message=message)
            print("✅ CHAT CREATED:", chat.id)  # ← add this

            return Response({
                'message': 'Message sent.',
                'chat': ChatSerializer(chat).data
            }, status=status.HTTP_201_CREATED)

        except jwt.ExpiredSignatureError:
            print("❌ TOKEN EXPIRED")  # ← add this
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            print("❌ INVALID TOKEN")  # ← add this
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("❌ UNEXPECTED ERROR:", str(e))  # ← add this — catches anything else
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# get chat history------------------------------------------------

class ChatHistoryView(APIView):
    def get(self,request , request_id):
        try:
            payload = decode_token(request)
            sender_type = payload.get('type')

            try:
                req = PartnerDonorRequest.objects.get(id=request_id)
            except PartnerDonorRequest.DoesNotExist:
                return Response(
                    {'error': 'Request not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Make sure this check allows both donor and partner
            if sender_type not in ['donor', 'partner']:
                return Response(
                {'error': 'Unauthorized.'},
                 status=status.HTTP_403_FORBIDDEN
                  )

# Verify sender belongs to this request
            if sender_type == 'donor':
                donor = Donor.objects.get(id=payload['id'])
                if req.assigned_donor != donor:
                  return Response(
            {'error': 'You are not assigned to this request.'},
            status=status.HTTP_403_FORBIDDEN
                               )
            elif sender_type == 'partner':
              partner = Partners.objects.get(id=payload['id'])
              if req.partner != partner:
                   return Response(
                    {'error': 'This request does not belong to you.'},
                        status=status.HTTP_403_FORBIDDEN
                   )
            chats = Chat.objects.filter(request=req).order_by('sent_at')
            return Response(ChatSerializer(chats, many=True).data)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
                
            

            
            



