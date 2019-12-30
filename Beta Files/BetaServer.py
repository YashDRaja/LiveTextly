import socket
from _thread import *
import pickle
import sys
from user import User
import copy

server = "192.168.1.22"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen() #NUMBER OF CONNECTIONS(PEOPLE)
print("Waiting for a connection, Server Started")

#connected  = set()
users = {}
idCount = 0

def threaded_client(conn,userId):
    global idCount
    conn.send(pickle.dumps(users[userId]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            #if users[userId].received[0] != None:
             #   print(users[userId].received, "recieved")
            data.received = users[userId].received
            users[userId] = data
            if not data:
                print("Disconnected")
                break
            else:

                if data.message[0] != None:
                    #print(data.message)
                    message = data.message
                    users[message[1]].received = (message[0],userId)
            u = copy.deepcopy(users[userId])
            users[userId].received = (None,None)
            conn.sendall(pickle.dumps(u))
        except:
            break
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    #idCount += 1
    #userId = (idCount -1)
    #users[userId] = User(userId)
    #print("Connecting Client", idCount)

    start_new_thread(threaded_client,(conn,userId))