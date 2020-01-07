import socket
from _thread import *
import pickle
import sys
from user import User
import copy

server = "192.168.1.22"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates socket for network to connect to

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen() #NUMBER OF CONNECTIONS(PEOPLE)
print("Waiting for a connection, Server Started")

users = {}
id_count = 0
def threaded_client(conn,y): #Creates new threaded client for each new client that is connecting
    new_list = list()
    for i in users.keys():
        new_list.append(i) #Users that already exists, for password check
    nl = []
    for i in new_list:
        nl.append([i,users[i].password])
    conn.send(pickle.dumps(nl)) #Users that exist are sent back
    user_id= conn.recv(2048).decode() #user id is established
    try:
        h = users[user_id] #Does this id exist, if not error is created transfers to except
    except:
        users[user_id] = User(user_id) #new user created for the new id
    conn.send(pickle.dumps(users[user_id])) #returns user associated with id

    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048)) #recieves client user
            data.received = users[user_id].received #updates client users messages received
            users[user_id] = data
            if not data: #Checks if connection active
                print("Disconnected")
                break
            else:

                if data.message[0] != None: #Checks to see if recipients are active or not
                    message = data.message
                    try:
                        h = users[message[1]] #if user active
                        users[message[1]].received = (message[0], user_id)
                    except:#if user not active, make active and deposit message, No password
                        users[message[1]] = User(message[1])
                        users[message[1]].history.append((message[0], user_id))


            u = copy.deepcopy(users[user_id])
            users[user_id].received = (None,None)
            conn.sendall(pickle.dumps(u))
        except:
            break


    conn.close() #Closes connectiong

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client,(conn,1)) #Creates new threaded client if there are new connections