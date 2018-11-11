class A(object):

    def __init__(self,a,b):
        self.a = a
        self.b = b

    def __hash__(self):
        return int(self.a)
    def __repr__(self):
        return str(self.a)
    def __eq__(self,other):
        print(self,other)
        return True

class B(object):
    
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def __hash__(self):
        return int(self.a)
    def __repr__(self):
        return str(self.a)
    def __eq__(self,other):
        print(self,other)
        return True
a = A(1,2)
b = A(1,3)

myset = set()

myset.add(a)
print(a in myset)

if b in myset:
    print("True")
else:
    print("False")