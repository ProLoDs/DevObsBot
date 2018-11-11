from pprint import pprint
from api.rocChatApi import WebsocketClient



client = WebsocketClient("ws://localhost/websocket", 'bot','test')