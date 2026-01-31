import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.room_group_name = f"chat_{self.room_name}"


        # Join room group
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # TODO: this is the part where we send the message to the AI model and 
        # get a response and send the response back and save the message to the DB
        message = text_data_json["message"]
        await self.send(json.dumps({"message": message}))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))