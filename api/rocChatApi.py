from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
import json
import time
from api.messages import *
from hashlib import sha256
from pprint import pprint
from api.util import Channel,generateRandomId


class WebsocketClient(object):
    def __init__(self, url, username, password, timeout=5):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.channels = set()
        self.ioloop = IOLoop.instance()
        self.openRequests = {}
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        PeriodicCallback(self.getChannels, 10000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print("connection error")
        else:
            print("connected")
            self.ws.write_message(CONNECT_MSG)
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            #pprint(msg)
            try:
                data = json.loads(msg)
                action = self.parseMessage(data)
                if action:
                    self.ws.write_message(action)
            except:
                raise
            if msg is None:
                print("connection closed")
                self.ws = None
                break

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            pass
            #self.ws.write_message("keep alive")

    def getChannels(self):
        reqId = generateRandomId()
        timestamp = time.time()
        self.openRequests[reqId] = self.handleGetChannels
        if not self.channels:
            timestamp = 0
        self.ws.write_message(GET_CHANNELS % (reqId,timestamp))
    
    def parseMessage(self, data):
        if u'msg' in data:
            if data[u'msg'] == u'ping':
                # print(json.dumps({u'msg':u'pong'}))
                return json.dumps({u'msg': u'pong'})
            elif data[u'msg'] == u'connected':
                reqId = generateRandomId()
                print("logging in with id",reqId)
                self.openRequests[reqId] = self.handleLogin
                hashedpw = sha256(self.password.encode('utf-8')).hexdigest()
                return LOGIN_MSG % (reqId,self.username, hashedpw)
            elif data[u'msg'] == u'result':
                if 'id' in data:
                    if int(data['id']) in self.openRequests:
                        self.openRequests[int(data['id'])](int(data['id']),data['result'])
                    else:
                        print("Unknown Id",data)
                else:
                    print("Strange result",data)
            else:
                print("Unknown msg")
                pprint(data)

        else:
            print("Totally Unknown",data)


    def handleLogin(self,reqId,data):
        pass
        #pprint(data)

    def handleGetChannels(self,reqId,data):
        for toBeRemoved in data[u'remove']:
            pass
        for toBeUpdated in data[u'update']:
            # pprint(toBeUpdated)
            print(toBeUpdated[u'_id'],toBeUpdated[u'_updatedAt'][u'$date'])
            c = Channel(toBeUpdated[u'_id'],int(toBeUpdated[u'_updatedAt'][u'$date']))
            if c not in self.channels:
                self.channels.add(c)
                reqId = generateRandomId()
                self.openRequests[reqId] = self.handleMessages
                self.ws.write_message(STREAM_ROOM % (reqId,toBeUpdated[u'_id']))
        #pprint(data)
    def handleMessages(self,reqId,data):
        print(data)

