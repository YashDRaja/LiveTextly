import pygame
from network import Network
from user import User
import pickle
pygame.init()
width = 500
height = 500
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Client")
def writeMessage(string,prev):
    #print(string)
    # name change
    #   font = pygame.font.SysFont("comicsans",40)
    #  name = font.render(string, True, (0,0,0))
    # win.blit(name, (50, 400))
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_BACKSPACE]:
        if len(string) != 0:
            string = string[:-1]
    if len(string) < 200:

        if pressed[pygame.K_RETURN]:
            return string, True
        elif pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]:
            if pressed[pygame.K_1]:
                string = string + "!"
            elif pressed[pygame.K_2]:
                string = string + "@"
            elif pressed[pygame.K_3]:
                string = string + "#"
            elif pressed[pygame.K_4]:
                string = string + "$"
            elif pressed[pygame.K_5]:
                string = string + "%"
            elif pressed[pygame.K_6]:
                string = string + "^"
            elif pressed[pygame.K_7]:
                string = string + "&"
            elif pressed[pygame.K_8]:
                string = string + "*"
            elif pressed[pygame.K_9]:
                string = string + "("
            elif pressed[pygame.K_0]:
                string = string + ")"
            elif pressed[pygame.K_MINUS]:
                string = string + "_"
            elif pressed[pygame.K_EQUALS]:
                string = string + "+"
            elif pressed[pygame.K_LEFTBRACKET]:
                string = string + "{"
            elif pressed[pygame.K_BACKSLASH]:
                string = string + "|"
            elif pressed[pygame.K_RIGHTBRACKET]:
                string = string + "}"
            elif pressed[pygame.K_SEMICOLON]:
                string = string + ":"
            elif pressed[pygame.K_QUOTE]:
                string = string + "\""
            elif pressed[pygame.K_COMMA]:
                string = string + "<"
            elif pressed[pygame.K_PERIOD]:
                string = string + ">"
            elif pressed[pygame.K_SLASH]:
                string = string + "?"
        elif pressed[pygame.K_SPACE]:
            string = string + " "
        elif pressed[pygame.K_QUOTE]:
            string = string + "\'"
        elif pressed[pygame.K_COMMA]:
            string = string + ","
        elif pressed[pygame.K_MINUS]:
            string = string + "-"
        elif pressed[pygame.K_PERIOD]:
            string = string + "."
        elif pressed[pygame.K_SLASH]:
            string = string + "/"
        elif pressed[pygame.K_SEMICOLON]:
            string = string + ";"
        elif pressed[pygame.K_EQUALS]:
            string = string + "="
        elif pressed[pygame.K_LEFTBRACKET]:
            string = string + "["
        elif pressed[pygame.K_BACKSLASH]:
            string = string + "\\"
        elif pressed[pygame.K_RIGHTBRACKET]:
            string = string + "]"
        # elif pressed[pygame.K_BACKSPACE]:
        #   string = string[:-1]
        elif pressed[pygame.K_BACKQUOTE]:
            string = string + "`"
        elif pressed[pygame.K_a]:
            string = string + "a"
        elif pressed[pygame.K_b]:
            string = string + "b"
        elif pressed[pygame.K_c]:
            string = string + "c"
        elif pressed[pygame.K_d]:
            string = string + "d"
        elif pressed[pygame.K_e]:
            string = string + "e"
        elif pressed[pygame.K_f]:
            string = string + "f"
        elif pressed[pygame.K_g]:
            string = string + "g"
        elif pressed[pygame.K_h]:
            string = string + "h"
        elif pressed[pygame.K_i]:
            string = string + "i"
        elif pressed[pygame.K_j]:
            string = string + "j"
        elif pressed[pygame.K_k]:
            string = string + "k"
        elif pressed[pygame.K_l]:
            string = string + "l"
        elif pressed[pygame.K_m]:
            string = string + "m"
        elif pressed[pygame.K_n]:
            string = string + "n"
        elif pressed[pygame.K_o]:
            string = string + "o"
        elif pressed[pygame.K_p]:
            string = string + "p"
        elif pressed[pygame.K_q]:
            string = string + "q"
        elif pressed[pygame.K_r]:
            string = string + "r"
        elif pressed[pygame.K_s]:
            string = string + "s"
        elif pressed[pygame.K_t]:
            string = string + "t"
        elif pressed[pygame.K_u]:
            string = string + "u"
        elif pressed[pygame.K_v]:
            string = string + "v"
        elif pressed[pygame.K_w]:
            string = string + "w"
        elif pressed[pygame.K_x]:
            string = string + "x"
        elif pressed[pygame.K_y]:
            string = string + "y"
        elif pressed[pygame.K_z]:
            string = string + "z"
        elif pressed[pygame.K_0]:
            string = string + "0"
        elif pressed[pygame.K_1]:
            string = string + "1"
        elif pressed[pygame.K_2]:
            string = string + "2"
        elif pressed[pygame.K_3]:
            string = string + "3"
        elif pressed[pygame.K_4]:
            string = string + "4"
        elif pressed[pygame.K_5]:
            string = string + "5"
        elif pressed[pygame.K_6]:
            string = string + "6"
        elif pressed[pygame.K_7]:
            string = string + "7"
        elif pressed[pygame.K_8]:
            string = string + "8"
        elif pressed[pygame.K_9]:
            string = string + "9"
    return string, False


def reDraw(win,string = None):
    win.fill((255,255,255))
    pygame.draw.rect(win, (128,128,128), (50,400,400,50))
    pygame.draw.rect(win, (68, 68, 68), (450, 400, 50, 50))
    if string != None:
        font = pygame.font.SysFont("comicsans", 40)
        name = font.render(string, True, (0, 0, 0))
        win.blit(name, (50, 400))
    pygame.display.update()
def main():
    run1 = True
    n = Network()
    c = n.getP()
    clock = pygame.time.Clock()
    print("id is",c.id)
    notSent = ""
    write = False
    send = False
    while run1:
        if c.id == 0:
            c.change(1)
        else:
            c.change(0)
        while True:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run1 = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if mouseX>= 50 and mouseX< 450 and mouseY >= 300 and mouseY <= 450:
                        write = True
                        prev = pygame.key.get_pressed()
                        notSent,send = writeMessage(notSent,prev)
                        if notSent == True:
                            run1 = False
                            break
                        if send == True:
                            mouseX = 450
                    if mouseX>= 450 and mouseX<= 500 and mouseY >= 300 and mouseY <= 450:
                        if notSent != "":
                            write = False
                            c.send(notSent)
                            notSent = ""
                    elif not(mouseX>= 50 and mouseX< 450 and mouseY >= 300 and mouseY <= 450):
                        write= False
                        c.send(None)
            if write:
                prev = pygame.key.get_pressed()
                notSent, send = writeMessage(notSent, prev)

            if send:
                write = False
                c.send(notSent)
                notSent = ""
            c = n.send(c)
            val = c.receive()
            if val != None:
                print(val[0], " by ", val[1])
            if notSent == "":
                reDraw(win)
            else:
                reDraw(win,notSent)



main()
