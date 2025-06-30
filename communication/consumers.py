import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_general'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from .models import Message
        from onboarding.models import Parent  # ✅ move import here

        data = json.loads(text_data)
        message = data['message']
        recipient_id = data['recipient_id']
        recipient = await database_sync_to_async(Parent.objects.get)(id=recipient_id)
        await database_sync_to_async(Message.objects.create)(
            sender=self.scope['user'],
            recipient=recipient,
            message_type='chat',
            content=message,
            delivered=True
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username,
                'recipient': recipient.name
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'recipient': event['recipient']
        }))
