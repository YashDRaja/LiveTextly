from network import Network
from user import User
import pickle
import multiprocessing
from tkinter import *
from scrollable import Scrollable
def send(queue1,queue2,textBox,sendButton):
    queue2.put((textBox.get(),0))
    textBox.delete(0,END)
def texts(queue1,queue2, scr,win):
    l = []
    while not queue1.empty():
        string = queue1.get()
        if string[1] == 1:
            if string[0] != "":
                label = Label(scr, text=string[0], justify=LEFT)
                label.pack()
        elif string[1] != None:
            l.append(string)
    if queue1.empty():
        queue1.put((None,None))
    while len(l) > 0:
        queue2.put(l[0])
        del l[0]
    scr.update()
    win.after(10, lambda: texts(queue1,queue2, scr,win))
def onClosing(q3,win1):
    q3.put("queue")
    win1.destroy()
def labelMake(win,txt):
    label = Label(win, text=txt)
    label.grid()
    label.after(1000, lambda: deleteL(label))
def changeId(e1,q4,win):
    try:
        num = e1.get()
        if num != "":
            q4.put(num)
        else:
            labelMake(win,"Give an Id")
    except:
        pass
def gui(queue1,queue2,queue3,queue4,idClient):
    win = Tk()
    sizex = 400
    sizey = 400
    posx = 100
    posy = 100
    win.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    txts = "client " + str(idClient)
    win.title(txts)
    scrF = Frame(win)
    scrF.grid(row=0, column=0,columnspan=3)
    screen = Scrollable(scrF,width=25)
    textBox = Entry()
    sendButton = Button(win, text="Send", pady=10, command=lambda: send(queue1,queue2,textBox,sendButton))  # padx, pady
    idBox = Entry()
    idButton = Button(win,text="change id", command=lambda: changeId(idBox,queue4,win))
    label1 = Label(win, text="Message")
    label2 = Label(win, text="Id")
    label1.grid(row=2,column=0)
    label2.grid(row=3, column=0)
    textBox.grid(row=2,column=1)
    sendButton.grid(row=2,column=2)
    win.after(0,lambda: texts(queue1,queue2,screen,win))
    win.protocol("WM_DELETE_WINDOW", lambda: onClosing(queue3,win))
    idBox.grid(row=3,column=1)
    idButton.grid(row=3,column=2)
    win.mainloop()
def passCheck(win1,e2,lis,id,li,n):
    y = li.index(id)
    if lis[y][1] == e2.get():
        n.idConf(id)
        win1.destroy()
    else:
        labelMake(win1, "Wrong Passwod")

def back(win1,l2,e2,b2,e1,n,b3):
    e1.config(state=NORMAL)
    l2.destroy()
    e2.destroy()
    b2.destroy()
    b3.destroy()
    b1 = Button(win1, text="Check/Save", command=lambda: idGetB(win1, e1, b1))
    b1.grid(row=1, column=0, columnspan=2)
def idGet(win,e1,n,b1):
    try:
        id = e1.get()
        if id == "":
            labelMake(win, "Give id")
            return
    except:
        pass
    l2 = n.idConfig()
    li = []
    l = []
    for y in l2:
        if y[1] != None:
            l.append(y)
    for x in l:
        li.append(x[0])
    if id in li:
        e1.config(state=DISABLED)
        b1.grid_forget()
        label2 = Label(win, text="Password")
        entry2 = Entry(win)
        button2 = Button(win, text="Check Password", command=lambda: passCheck(win, entry2,l,str(id),li,n))
        button3 = Button(win, text="Back", command=lambda: back(win, label2, entry2, button2,e1,n,button3))
        label2.grid(row=1, column=0)
        entry2.grid(row=1, column=1)
        button3.grid(row=2,column=0)
        button2.grid(row=2, column=1)
    else:
        n.idConf(id)
        e1.config(state=DISABLED)
        b1.destroy()
        l2 = Label(win, text="Password")
        e2 = Entry()
        b2 = Button(win, text="Save Password", command=lambda: passSet(win,e2,n))
        l2.grid(column=0, row=1)
        e2.grid(column=1, row=1)
        b2.grid(row=2, column=0, columnspan=2)
def idGetB(win,e1,b1):
    global n
    n = Network()
    idGet(win,e1,n,b1)
def passSet(win1,e2,n):
    c = n.getP()
    c.password = e2.get()
    win1.destroy()
def deleteL(label):
    label.destroy()
def closed():
    win1 = Tk()
    win1.title("Select id")
    l1 = Label(win1, text="ID")
    e1 = Entry()
    b1 = Button(win1, text="Check/Save", command=lambda: idGet(win1, e1, n, b1))
    l1.grid(column=0, row=0)
    e1.grid(column=1, row=0)
    b1.grid(row=1, column=0, columnspan=2)
    win1.mainloop()
def main():
    run1 = True
    closed()
    try:
        c = n.getP()
    except:
        return
    c.change(c.id)
    write = False
    string = ""
    p = multiprocessing.Process(target= gui,args=[queue1,queue2,queue3,queue4,c.id])
    p.start()
    his = c.history
    for val in his:
        queue1.put((val[0] + " by " + str(val[1]), 1))
    while True:
        if not (queue4.empty()):
            numb = queue4.get()
            c.change(str(numb))
        if not(queue3.empty()):
            run1 = False
            u = queue3.get()
            break
        c = n.send(c)
        val = c.receive()
        if val != None:
            queue1.put((val[0]+ " by "+str(val[1]),1))
        l = []
        while not queue2.empty():
            string = queue2.get()
            if string[1] == 0:
                if string[0] != "":
                    c.send(string[0])
            elif string[1] != None:
                l.append(string)
        if queue2.empty():
            queue2.put((None, None))
        while len(l) > 0:
            queue1.put(l[0])
            del l[0]

global n
if __name__ == "__main__":
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    queue3 = multiprocessing.Queue()
    queue4 = multiprocessing.Queue()
    n = Network()
    main()
