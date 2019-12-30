from network import Network
from user import User
import pickle
import multiprocessing
from tkinter import *

def send(queue1,queue2,textBox,sendButton):
    queue2.put((textBox.get(),0))
    textBox.delete(0,END)
def texts(queue1,queue2, scr,win):
    l = []
    while not queue1.empty():
        string = queue1.get()
        #print(string, "here")
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
    win.after(10, lambda: texts(queue1,queue2, scr,win))
def gui(queue1,queue2):
    win = Tk()
    sizex = 800
    sizey = 600
    posx = 100
    posy = 100
    win.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    win.title("client")
    screen = Frame(win)
    textBox = Entry()
    sendButton = Button(win, text="Send", pady=10, command=lambda: send(queue1,queue2,textBox,sendButton))  # padx, pady
    screen.grid(row=0, column=0)
    textBox.grid(row=1,column=0)
    sendButton.grid(row=1,column=1)
    win.after(0,lambda: texts(queue1,queue2,screen,win))
    win.mainloop()

def main():
    run1 = True
    n = Network()
    c = n.getP()
    print("id is",c.id)
    write = False
    string = ""
    p = multiprocessing.Process(target= gui,args=[queue1,queue2])
    p.start()
    while run1:

        if c.id == 0:
            c.change(1)
        else:
            c.change(0)
        while True:
            c = n.send(c)
            val = c.receive()
            if val != None:
                queue1.put((val[0]+ " by "+str(val[1]),1))
            l = []
            while not queue2.empty():
                string = queue2.get()
                #print(string, "hey")

                if string[1] == 0:
                    if string[0] != "":
                        #print(string[0])
                        c.send(string[0])
                elif string[1] != None:
                    l.append(string)
            if queue2.empty():
                queue2.put((None, None))
            while len(l) > 0:
                queue1.put(l[0])
                del l[0]

if __name__ == "__main__":
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    main()
