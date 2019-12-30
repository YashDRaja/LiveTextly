import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "192.168.1.22"
        self.port = 5555
        self.addr= (self.server, self.port)
        #self.p = self.connect()
        self.connected = False
    def getP(self):
        return self.p
    def idConfig(self):
        try:
            if self.connected == False:
                self.client.connect(self.addr)
                self.connected = True
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    def idConf(self,data):
        self.client.send(str.encode(str(data)))
        self.p = self.connect()
    def connect(self):
        try:
            if self.connected == False:
                self.client.connect(self.addr)
                self.connected = True
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    def send(self,data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)