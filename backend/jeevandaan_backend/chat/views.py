from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer
from requests_app.models import PartnerDonorRequest
from users.models import Donor
from partners.models import Partners


from config.authentication import AnyJWTAuthentication
from config.permissions import IsAuthenticated



#sendmaeesage -----------------

class SendMessageView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, request_id):
        try:
            user = request.user
            
            if isinstance(user, Partners):
                sender_type = 'partner'
            elif isinstance(user, Donor):
                sender_type = 'donor'
            else:
                return Response({'error': 'Invalid user'}, status=403)
            
            

            try:
                req = PartnerDonorRequest.objects.get(id=request_id)
                
            except PartnerDonorRequest.DoesNotExist:
                return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            if req.status in ['fulfilled', 'expired', 'cancelled']:
                
                return Response({'error': 'Chat is closed for this request.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if sender_type == 'donor':
                donor = user
                
                if req.assigned_donor != donor:
                    
                    return Response({'error': 'You are not assigned to this request.'}, status=status.HTTP_403_FORBIDDEN)
            
            elif sender_type == 'partner':
                partner = user
                
                if req.partner != partner:
                    
                    return Response({'error': 'This request does not belong to you.'}, status=status.HTTP_403_FORBIDDEN)

            message = request.data.get('message')
            
            
            valid_messages = [
                'on_the_way', 'reached', 'unable_to_come', 'delayed', 'donated',
                'waiting_for_donor', 'donor_arrived', 'please_hurry',
                'donation_received', 'request_cancelled'
            ]
            if message not in valid_messages:
                
                return Response({'error': 'Invalid message.'}, status=status.HTTP_400_BAD_REQUEST)
            
            chat = Chat.objects.create(request=req, sender_type=sender_type, message=message)
           

            return Response({
                'message': 'Message sent.',
                'chat': ChatSerializer(chat).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(" UNEXPECTED ERROR:", str(e)) 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# get chat history------------------------------------------------

class ChatHistoryView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        try:
            user = request.user


            if isinstance(user, Partners):
                sender_type = 'partner'
            elif isinstance(user, Donor):
                sender_type = 'donor'
            else:
                return Response({'error': 'Invalid user'}, status=403)
            

            try:
                req = PartnerDonorRequest.objects.get(id=request_id)
            except PartnerDonorRequest.DoesNotExist:
                return Response(
                    {'error': 'Request not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            
            if sender_type == 'donor':
                donor = user
                if req.assigned_donor != donor:
                    return Response(
                        {'error': 'You are not assigned to this request.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            elif sender_type == 'partner':
                partner = user
                if req.partner != partner:
                    return Response(
                        {'error': 'This request does not belong to you.'},
                        status=status.HTTP_403_FORBIDDEN
                    )

            chats = Chat.objects.filter(request=req).order_by('sent_at')
            return Response(
                ChatSerializer(chats, many=True).data,
                status=status.HTTP_200_OK  
            )

        
        except Exception as e:
            print(" CHAT HISTORY ERROR:", str(e))  # shows in Render logs
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


