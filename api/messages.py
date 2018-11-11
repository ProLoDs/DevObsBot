CONNECT_MSG = '''{
    "msg": "connect",
    "version": "1",
    "support": ["1"]
}'''


LOGIN_MSG = '''{
    "msg": "method",
    "method": "login",
    "id":"%s",
    "params":[
        {
            "user": { "username": "%s" },
            "password": {
                "digest": "%s",
                "algorithm":"sha-256"
            }
        }
    ]
}'''

GET_CHANNELS = '''{
    "msg": "method",
    "method": "rooms/get",
    "id": "%s",
    "params": [ { "$date": %s } ]
}'''

STREAM_ROOM = '''{
    "msg": "sub",
    "id": "%s",
    "name": "stream-room-messages",
    "params":[
        "%s",
        false
    ]
}'''