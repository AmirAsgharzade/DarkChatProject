import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from Authen.models import CustomUser
from GlobeChat.models import GlobeHistory

def create_message(**data):
    instance = GlobeHistory(**data)
    instance.save()
    print('added message')
    return instance

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_group_name = 'global_chat'

        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,self.channel_name
        )

        await self.accept() #accept websocket connection

    async def disconnect(self,close_code):
        #leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']
        content = text_data_json['content']
        color = text_data_json['color']

        user = await self.get_user(username)
        print(user.username)
        if user:
            instance = await database_sync_to_async(create_message)(
            user=user,username=user.username,color=user.color,content=content
            )
            cache.delete('messages')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'username':username,
                'content':content,
                'color':color
            }
        )
    
    async def chat_message(self,event):
        message = event['content']
        username = event['username']
        color = event['color']
        await self.send(text_data=json.dumps({
            'username':username,
            'content':message,
            'color':color
        }))

    async def get_user(self,username):
        return await database_sync_to_async(CustomUser.objects.get)(username=username)
