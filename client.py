from network import Network
from user import User
import pickle
import multiprocessing
from tkinter import *
from scrollable import Scrollable


def texts(queue1,queue2, scr,win):
    l = []
    while not queue1.empty(): #Messages recieved
        string = queue1.get()
        if string[1] == 1:
            if string[0] != "":
                label = Label(scr, text=string[0], justify=LEFT)
                label.pack()
        elif string[1] != None:
            l.append(string)
    if queue1.empty():
        queue1.put((None,None))
    while len(l) > 0: #If message not sent, stores message to send
        queue2.put(l[0])
        del l[0]
    scr.update()
    win.after(10, lambda: texts(queue1,queue2, scr,win))


def send(queue1,queue2,textBox,sendButton):#Sends message to recipient
    queue2.put((textBox.get(),0))
    textBox.delete(0,END)


def on_closing(q3,win1): #Closes client connection
    q3.put("queue")
    win1.destroy()


def label_make(win,txt): #Displays warning for 1 second
    label = Label(win, text=txt)
    label.grid()
    label.after(1000, lambda: delete_l(label))


def change_id(e1,q4,win): # Change id for user
    try:
        num = e1.get()
        if num != "":
            q4.put(num)
        else:
            label_make(win,"Give an Id")
    except:
        pass


def gui(queue1,queue2,queue3,queue4,id_client):
    win = Tk()
    size_x = 400
    size_y = 400
    pos_x = 100
    pos_y = 100
    win.wm_geometry("%dx%d+%d+%d" % (size_x, size_y, pos_x, pos_y))
    txts = "client " + str(id_client)
    win.title(txts)
    scr_frame = Frame(win)
    scr_frame.grid(row=0, column=0,columnspan=3)
    screen = Scrollable(scr_frame,width=25)
    text_box = Entry()
    send_button = Button(win, text="Send", pady=10, command=lambda: send(queue1,queue2,text_box,send_button))  # padx, pady
    id_box = Entry()
    id_button = Button(win,text="change id", command=lambda: change_id(id_box,queue4,win))
    label1 = Label(win, text="Message")
    label2 = Label(win, text="Id")
    label1.grid(row=2,column=0)
    label2.grid(row=3, column=0)
    text_box.grid(row=2,column=1)
    send_button.grid(row=2,column=2)
    win.after(0,lambda: texts(queue1,queue2,screen,win))
    win.protocol("WM_DELETE_WINDOW", lambda: on_closing(queue3,win))
    id_box.grid(row=3,column=1)
    id_button.grid(row=3,column=2)
    win.mainloop()


def pass_check(win1,e2,lis, id, li,n): #Checks if password is correct for the id
    y = li.index(id)
    if lis[y][1] == e2.get():
        n.id_conf(id)
        win1.destroy()
    else:
        label_make(win1, "Wrong Passwod")


def back(win1,l2,e2,b2,e1,n,b3): #If user wants to change which id is being logged in
    e1.config(state=NORMAL)
    l2.destroy()
    e2.destroy()
    b2.destroy()
    b3.destroy()
    b1 = Button(win1, text="Check/Save", command=lambda: id_get_b(win1, e1, b1))
    b1.grid(row=1, column=0, columnspan=2)


def id_get(win,e1,n,b1):
    try: #Finds id that is given by user
        id = e1.get()
        if id == "":
            label_make(win, "Give id")
            return
    except:
        pass
    #Checks if id exists and if it does what is it's password
    l2 = n.id_config()
    li = []
    l = []
    try:
        for y in l2:
            if y[1] != None:
                l.append(y)
    except:
        print("The Server is N/a")
    for x in l:
        li.append(x[0])
    if id in li:#Checks password which is inputed against the password for the id
        e1.config(state=DISABLED)
        b1.grid_forget()
        label2 = Label(win, text="Password")
        entry2 = Entry(win)
        button2 = Button(win, text="Check Password", command=lambda: pass_check(win, entry2,l,str(id),li,n))
        button3 = Button(win, text="Back", command=lambda: back(win, label2, entry2, button2,e1,n,button3))
        label2.grid(row=1, column=0)
        entry2.grid(row=1, column=1)
        button3.grid(row=2,column=0)
        button2.grid(row=2, column=1)
    else:#saves the password as the password for the id
        n.id_conf(id)
        e1.config(state=DISABLED)
        b1.destroy()
        l2 = Label(win, text="Password")
        e2 = Entry()
        b2 = Button(win, text="Save Password", command=lambda: pass_set(win,e2,n))
        l2.grid(column=0, row=1)
        e2.grid(column=1, row=1)
        b2.grid(row=2, column=0, columnspan=2)


def id_get_b(win,e1,b1): #switching client Id numbers requires new network
    global n
    n = Network()
    id_get(win,e1,n,b1)


def pass_set(win1,e2,n): #sets password for client/id
    c = n.getP()
    c.password = e2.get()
    win1.destroy()


def delete_l(label): #Deletes labels such as warnings
    label.destroy()


def start():
    win1 = Tk()
    win1.title("Select id")
    l1 = Label(win1, text="ID")
    e1 = Entry()
    b1 = Button(win1, text="Check/Save", command=lambda: id_get(win1, e1, n, b1)) #Checks or Saves Id
    l1.grid(column=0, row=0)
    e1.grid(column=1, row=0)
    b1.grid(row=1, column=0, columnspan=2)
    win1.mainloop()


def main():
    start() #Lets user log onto a id from the server
    try:
        c = n.getP() #Connects to server via network
    except:
        return #Server unavaible
    c.change(c.id)
    string = ""
    p = multiprocessing.Process(target= gui,args=[queue1, queue2, queue3, queue4, c.id]) #Intializes gui process
    p.start() #Starts gui process
    his = c.history #finds messages the server has already recieved for this client id
    for val in his:
        queue1.put((val[0] + " by " + str(val[1]), 1)) #Queue1 takes data sends to gui and outputs, the data being the history
    while True:
        if not (queue4.empty()): #Checks recipient for the message in queue4
            numb = queue4.get()
            c.change(str(numb))
        if not(queue3.empty()): #GUI communication to terminate program
            u = queue3.get()
            break
        c = n.send(c) #Sending server client, receiving updated client from server
        val = c.receive() #messages recieved from others
        if val != None:
            queue1.put((val[0]+ " by "+str(val[1]),1)) #New messages are communicated to gui
        l = []
        while not queue2.empty(): #Queue2 responsible for communicating what messages are being sent to others
            string = queue2.get()
            if string[1] == 0:
                if string[0] != "":
                    c.send(string[0])
            elif string[1] != None:
                l.append(string)
        if queue2.empty():
            queue2.put((None, None))
        while len(l) > 0:#Only 1 message is sent at a time if any not sent then stored to be sent
            queue1.put(l[0])
            del l[0]

global n
if __name__ == "__main__": #Runs only in main process
    queue1 = multiprocessing.Queue() #Queues used to data transfer between processes
    queue2 = multiprocessing.Queue()
    queue3 = multiprocessing.Queue()
    queue4 = multiprocessing.Queue()
    n = Network() #initializes the network class
    main()
