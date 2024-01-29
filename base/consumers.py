# your_app/consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class BalanceUpdateConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         student_id = data.get('student_id')

#         # You may need to implement your own logic to fetch the student's balance
#         # and send it to the client

#         await self.send(text_data=json.dumps({'balance': updated_balance}))



# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . models import Student
class BalanceUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the connected user to the balance_updates_group
        await self.channel_layer.group_add(
            'balance_updates_group',
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Remove the connected user from the balance_updates_group
        await self.channel_layer.group_discard(
            'balance_updates_group',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        student_id = data.get('student_id')

        # You may need to implement your own logic to fetch the student's balance
        # and send it to the client
        updated_balance = await self.get_student_balance(student_id)

        await self.send(text_data=json.dumps({'balance': updated_balance}))

    @database_sync_to_async
    def get_student_balance(self, student_id):
        # Implement your logic to fetch the student's balance from the database
        # This should be a database query to get the latest balance
        # For example, if your model has a field named 'balance', you can do:
        return Student.objects.get(id=student_id).balance
