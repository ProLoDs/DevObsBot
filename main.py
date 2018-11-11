from api.rocChatApi import WebsocketClient


class testHandler(object):
    def __init__(self):
        self.prefix = "!test"

    def __call__(self, room, username, msg):
        print("Inside testHandler:", room, username, msg)


class testHandler2(object):
    def __init__(self):
        self.prefix = "!test2"

    def __call__(self, room, username, msg):
        print("Inside testHandler 2:", room, username, msg)


t = testHandler()
t2 = testHandler2()
myHandlers = {}


def addHandler(*handlers):
    for handler in handlers:
        myHandlers[handler.prefix] = handler


addHandler(t, t2)

client = WebsocketClient("ws://localhost/websocket", 'bot', 'test', myHandlers)
client.start()
