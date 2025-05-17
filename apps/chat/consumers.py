import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q

from apps.chat.models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        user = self.scope["user"]

        if not await self.is_participant(user.id):
            await self.close()
            return

        self.room_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def is_participant(self, user_id):
        return Chat.objects.filter(
            Q(participant1_id=user_id) | Q(participant2_id=user_id),
            id=self.chat_id
        ).exists()

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        handlers = {
            'message': self.handle_message,
            'read_receipt': self.handle_read_receipt,
            'webrtc_offer': self.handle_webrtc_offer,
            'webrtc_answer': self.handle_webrtc_answer,
            'ice_candidate': self.handle_ice_candidate
        }

        await handlers[event_type](data)

    # Обработка сообщений
    async def handle_message(self, data):
        message = await self.create_message(data)
        await self.send_message_to_group(message)

    async def create_message(self, data):
        return await database_sync_to_async(Message.objects.create)(
            chat_id=self.chat_id,
            sender=self.scope['user'],
            text=data.get('text', '')
        )

    async def send_message_to_group(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': await self.message_data(message)
            }
        )

    # Подтверждение прочтения
    async def handle_read_receipt(self, data):
        message = await database_sync_to_async(Message.objects.get)(id=data['message_id'])
        message.is_read = True
        await database_sync_to_async(message.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'read_receipt',
                'message_id': data['message_id']
            }
        )

    # WebRTC обработчики
    async def handle_webrtc_offer(self, data):
        await self.send_to_recipient({
            'type': 'webrtc_offer',
            'offer': data['offer'],
            'caller': self.scope['user'].id
        })

    async def handle_webrtc_answer(self, data):
        await self.send_to_recipient({
            'type': 'webrtc_answer',
            'answer': data['answer']
        })

    async def handle_ice_candidate(self, data):
        await self.send_to_recipient({
            'type': 'ice_candidate',
            'candidate': data['candidate']
        })

    async def send_to_recipient(self, payload):
        await self.channel_layer.group_send(
            self.room_group_name,
            {**payload, 'sender_channel': self.channel_name}
        )

    # Хэлперы
    async def chat_message(self, event):
        if self.channel_name != event.get('sender_channel'):
            await self.send(text_data=json.dumps(event['message']))

    async def message_data(self, message):
        return {
            'type': 'message',
            'id': message.id,
            'text': message.text,
            'sender': message.sender.username,
            'timestamp': str(message.timestamp),
            'files': [
                {'url': file.file.url, 'type': file.file_type}
                for file in message.files.all()
            ]
        }

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        if event_type in ['offer', 'answer', 'ice-candidate']:
            await self.handle_webrtc_signal(data)
        else:
            await super().receive(text_data)

    async def handle_webrtc_signal(self, data):
        # Отправляем сигнал другому участнику чата
        other_user = self.get_other_user()
        await self.channel_layer.send(
            f"user_{other_user.id}",
            {
                "type": "webrtc.signal",
                "signal": data
            }
        )

    async def webrtc_signal(self, event):
        await self.send(text_data=json.dumps(event["signal"]))

    # consumers.py
    async def send_notification(self, notification_data):
        await self.channel_layer.group_send(
            f"user_{self.user.id}",
            {
                "type": "send.notification",
                "notification": notification_data
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'NOTIFICATION',
            'data': event['notification']
        }))
