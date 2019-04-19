import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        """when the socket connects"""
        print("connected", event)
        # doing await means that it's going
        # to execute that code and wait for it
        # to finish
        await self.send({
            'type': 'websocket.accept'
        })

        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        print(other_user, me)
        thread_obj = await self.get_thread(
            me,
            other_user
        )
        print(thread_obj)

        # close the connection
        await self.send({
            'type': 'websocket.send',
            'text': 'Hello world'
        })

    async def websocket_receive(self, event):
        """when a message is received from a websocket"""
        print("receive", event)

    async def websocket_disconnect(self, event):
        """when the socket disconnects"""
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(
            user,
            other_username
        )[0]

