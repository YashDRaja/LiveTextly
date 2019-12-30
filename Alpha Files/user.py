class User:
    def __init__(self, id):
        self.id = id
        self.receiver = None
        self.received = (None,None)
        self.history = []
        self.message = (None,self.receiver)
        self.sent = []
    def receive(self):
        if self.message[0] != None:
            self.sent.append(self.message)
            self.message = (None,self.receiver)
        if self.received[0] != None:
            message = self.received
            self.history.append(self.received)
            self.received = (None,None)
            return message
    def send(self,message):
        self.message = (message,self.receiver)
    def change(self,id):
        self.receiver = id


