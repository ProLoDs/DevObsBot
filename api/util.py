import random
class Channel(object):
    def __init__(self,id,lastMessage):
        self.id = id
        self.lastMessage = lastMessage

    def __eq__(self,other):
        if hasattr(other, 'id'):
            if self.id == other.id:
                return True
        return False
    def __hash__(self):
        return hash(self.id)

def generateRandomId():
    return random.randint(0,1<<32)