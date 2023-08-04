import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatModel

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f"{other_user_id}-{my_id}"
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )    
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(message=message, thread_name=self.room_group_name, username=username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendMessage',
                'message': message,
                'username': username
            }
        )

    async def sendMessage(self , event) :
        message = event["message"]
        username = event["username"]
        await self.send(text_data = json.dumps({"message":message , "username":username}))

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        ChatModel.objects.create(
            sender=username, message=message, thread_name=thread_name)

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.roomGroupName = "group_chat_gfg"
#         await self.channel_layer.group_add(
#             self.roomGroupName ,
#             self.channel_name
#         )
#         await self.accept()
#     async def disconnect(self , close_code):
#         await self.channel_layer.group_discard(
#             self.roomGroupName ,
#             self.channel_layer
#         )
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]
#         await self.channel_layer.group_send(
#             self.roomGroupName,{
#                 "type" : "sendMessage" ,
#                 "message" : message ,
#                 "username" : username ,
#             })
#     async def sendMessage(self , event) :
#         message = event["message"]
#         username = event["username"]
#         await self.send(text_data = json.dumps({"message":message ,"username":username}))