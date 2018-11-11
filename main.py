from pprint import pprint
from api.rocChatApi import WebsocketClient

class testHandler(object):
    def __init__(self):
        self.prefix = "!test"

    def __call__(self,room,username,msg):
        print("Inside testHandler",room,username,msg)


client = WebsocketClient("ws://localhost/websocket", 'bot','test')
client.addhandler(testHandler)