from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("Connection Called")
        self.room_group_name = "chat" #'chat_%s' % self.room_name

        # 그룹에 join
        # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야한다.
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # WebSocket 연결
        self.accept()

    def disconnect(self, close_code):
        # 그룹에서 Leave
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # WebSocket 에게 메세지 receive
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # room group 에게 메세지 send
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message +" __ from server!!"
            }
        )

    # room group 에서 메세지 receive
    def chat_message(self, event):
        message = event['message']

        # WebSocket 에게 메세지 전송
        self.send(text_data=json.dumps({
            'message': message
        }))