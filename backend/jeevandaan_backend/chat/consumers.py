from channels.generic.websocket import AsyncWebsocketConsumer
import json


from channels.db import database_sync_to_async
from requests_app.models import PartnerDonorRequest
from users.models import Donor
from partners.models import Partners
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
      user = self.scope.get("user")

      if user is None:
        await self.close(code=4001)
        return
      

      self.request_id = self.scope["url_route"]["kwargs"]["request_id"]
      self.room_group_name = f"chat_{self.request_id}"

      if not await self.is_authorized(user):
       await self.close(code=4003)
       return

      await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name,
    )

      await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def chat_message(self, event):
        await self.send(
          text_data=json.dumps(event["message"], default=str)
    )

    @database_sync_to_async
    def is_authorized(self, user):
        try:
            req = PartnerDonorRequest.objects.select_related(
            "assigned_donor",
            "partner"
            ).get(id=self.request_id)

            if req.status in ["fulfilled", "expired", "cancelled"]:
               return False

            if isinstance(user, Donor):
               return req.assigned_donor_id == user.id

            if isinstance(user, Partners):
                return req.partner_id == user.id

            return False

        except PartnerDonorRequest.DoesNotExist:
            return False
        
    