from tkinter import *
import tkinter.messagebox as mbox 
from tkinter import ttk, filedialog
import tkinter as tk
import socket
import threading
from PIL import Image
import numpy as np
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE = "DISCONNECT!"
TAKE_SCREEN_SHOT = "TAKE SCREENSHOT"
RUNNING_PROCESS ="CHECK RUNNING PROCESS"
RUNNING_APP ="CHECK RUNNING APP"
STOP_LISTING = "STOP"
START_LISTING = "START LISTING"
KILL_APP_VIA_PID = "KILL APP VIA PID"
KILL_PROCESS_VIA_PID = "KILL PROCESS VIA PID"
KILL_PROCESS_VIA_NAME = "KILL PROCESS VIA NAME"
START_PROCESS = "START PROCESS"
KEYLOGGING ="KEY LOG"
STOP_KEYLOGGING = "STOP KEYLOGGING"
PRINT_KEYLOG = "PRINT KEYLOG"
SHUTDOWN = "SHUTDOWN"
CANCEL_SHUTDOWN = "CANCEL SHUTDOWN"
SEND_FILE = "SEND FILE"
SEND_REG_FILE = "SEND REG FILE"
DELETE_KEY_VALUE = "DELETE REG VALUE"
GET_KEY_VALUE = "GET KEY VALUE"
ADD_NEW_KEY = "ADD NEW KEY"
DELETE_KEY = "DELETE KEY"
SET_KEY_VALUE ="SET KEY VALUE"



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
                file.close()
                break
            if size - i < 1024:
                byte_read = size - i

def recv_file1(conn,filename):
    size = recv1(conn)
    size = int(size)
    t = size/2
    t= int(t)
    with open(filename,'wb') as file:
        for i in range(t):
            data = conn.recv(2)
            file.write(data)







TITLE = "Client "

connected =False




 #ProcessRunning------------------------------------------------------------------------------------------

def doProcessRunning():
    global connected
    if connected == True:
        proc_name_l, pid_l, thread_cnt_l = [], [], []
        count = 0

        def KILL_PR():


            def KILL_PR_EXECUTE(event):
                send(KILL_PROCESS_VIA_PID)
                kill_this_pid = entry.get()
                send1(client,str(kill_this_pid))
                succeed = recv1(client)
                if succeed == "True":
                    
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

            
            
        
        def SHOW_PR():
            send(RUNNING_PROCESS)
            size = recv1(client)
            size = int(size)
            for i in range(size):
                name = recv1(client)
                pid = recv1(client)
                threadCount =recv1(client)
                
                tree.insert('', 'end', iid= i, text="" , values=(name,pid,threadCount))
                
            
        
        def DELETE_PR():
            for i in tree.get_children():
                tree.delete(i)
            

        def START_PR():
            def START_PR_EXECUTE():
                send(START_PROCESS)
                proc = entry.get()
                send1(client, proc)
                

            RootPR_START = Toplevel(RootPR)

            RootPR_START.title(40*" "+"START")
            RootPR_START.geometry("400x50")
            RootPR_START.resizable(0, 0)
            RootPR_START.grab_set()
            
            entry = Entry(RootPR_START, width = 40)
            buttonPR_START_InSide = Button(RootPR_START, text = "START",width=10, height = 1, command = START_PR_EXECUTE)

            entry.place(x = 20, y = 15)
            buttonPR_START_InSide.place(x = 280, y = 15)

        #------------------------------------------------------
        RootPR = Toplevel(Client_windows)
        RootPR.title(55*" "+"Process")
        RootPR.grab_set()

        RootPR.geometry("500x350")
        
        #KILL
        buttonPR_KILL = Button(RootPR, text = 'KILL',padx =33, pady=20, command= KILL_PR)
        buttonPR_KILL.place(x =38, y =15)

        #SHOW
        buttonPR_SHOW = Button(RootPR, text = 'SHOW',padx =28, pady=20, command = SHOW_PR)
        buttonPR_SHOW.place(x =140, y =15)

        #DELETE
        buttonPR_SHOW = Button(RootPR, text = 'DELETE',padx =27, pady=20, command = DELETE_PR)
        buttonPR_SHOW.place(x =245, y =15)

        #Start
        buttonPR_SHOW = Button(RootPR, text = 'START',padx =33, pady=20, command= START_PR)
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
    else:
        mbox.showinfo(None,"No connection established!")

#APPRunning-----------------------------------------------------------------------------------------------

def doAPPRunning():
    global connected
    if connected == True:

        def KILL_AR():

            def KILL_PR_EXECUTE():
                send(KILL_PROCESS_VIA_PID)
                kill_this_pid = entry.get()
                send1(client,str(kill_this_pid))
                succeed = recv1(client)
                if succeed == "True":
                    
                    mbox.showinfo(None,"Operation compeleted")
                else:
                    mbox.showinfo(None,"Process not found")

            
            RootAR_KILL = Toplevel(RootAR)
            RootAR_KILL.title(40*" "+"KILL")
            RootAR_KILL.geometry("400x50")
            RootAR_KILL.resizable(0, 0)
            RootAR_KILL.grab_set()

            entry = Entry(RootAR_KILL, width = 40)
            buttonAR_KILL_InSide = Button(RootAR_KILL, text = "KILL",width=10, height = 1, command= KILL_PR_EXECUTE)

            entry.place(x = 20, y = 15)
            buttonAR_KILL_InSide.place(x = 280, y = 15)

        def SHOW_AR():
            
            send(RUNNING_APP)
            msg = recv1(client)
            if msg == "No running app!":
                mbox.showinfo(None,'No applications running on server os!')
            else:
                size = int(msg)
                for i in range(size):
                    name = recv1(client)
                    pid = recv1(client)
                    threadCount =recv1(client)
                    
                    tree.insert('', 'end', iid= i, text="" , values=(name,pid,threadCount))
                

        def DELETE_AR():
            for i in tree.get_children():
                tree.delete(i)

        def START_AR():
            def START_AR_EXECUTE():
                send(START_PROCESS)
                proc = entry.get()
                send1(client, proc)

            
            RootAR_START = Toplevel(RootAR)
            RootAR_START.title(40*" "+"START")
            RootAR_START.geometry("400x50")
            RootAR_START.resizable(0, 0)
            RootAR_START.grab_set()

            entry = Entry(RootAR_START, width = 40)
            buttonAR_START_InSide = Button(RootAR_START, text = "START",width=10, height = 1, command= START_AR_EXECUTE)

            entry.place(x = 20, y = 15)
            buttonAR_START_InSide.place(x = 280, y = 15)

        #--------------------------------------------
        RootAR = Toplevel(Client_windows)
        RootAR.title(55*" "+"ListApp")
        RootAR.grab_set()
        RootAR.geometry("500x350")
        #KILL
        buttonAR_KILL = Button(RootAR, text = 'KILL',padx =33, pady=20,command= KILL_AR)
        buttonAR_KILL.place(x =38, y =15)
        #SHOW
        buttonPR_SHOW = Button(RootAR, text = 'SHOW',padx =28, pady=20, command= SHOW_AR)
        buttonPR_SHOW.place(x =140, y =15)
        #DELETE
        buttonPR_SHOW = Button(RootAR, text = 'DELETE',padx =27, pady=20, command= DELETE_AR)
        buttonPR_SHOW.place(x =245, y =15)
        #Start
        buttonPR_SHOW = Button(RootAR, text = 'START',padx =33, pady=20, command= START_AR)
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
    else:
        mbox.showinfo(None,"No connection established!")

#KEYSTROKE------------------------------------------------------------------------------------------------


hooked = False

def doKEYSTROKE():
    global connected
    if connected == True:

        def HOOK():
            global hooked
            hooked=True
            send1(client,KEYLOGGING)
            
        def A():
            threading.Thread(target=HOOK).start()



        def UNHOOK():  
            global hooked
            hooked = False
            send1(client,STOP_KEYLOGGING)

        def B():
            threading.Thread(target=UNHOOK).start()



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
        buttonK_HOOK.place(x =38, y =15)

        #UNHOOK
        buttonK_UNHOOK = Button(RootK, text = 'UNHOOK',padx =33, pady=20, command= B)
        buttonK_UNHOOK.place(x =140, y =15)

        #PRINT
        buttonK_PRINT = Button(RootK, text = 'PRINT',padx =33, pady=20, command= C)
        buttonK_PRINT.place(x =245, y =15)

        #DELETE
        buttonK_DELETE = Button(RootK, text = 'DELETE',padx =33, pady=20, command=D)
        buttonK_DELETE.place(x =350, y =15)
    
        #TABLE
        text = Text(RootK)
        text.place(x = 38, y = 90, width = 425, height = 230)
    else:
        mbox.showinfo(None,"No connection established!")

#FixRegistry----------------------------------------------------------------------------
def doFixRegistry():
    global connected
    if connected == True:
        # current_function ={1 : Get value
        #                    2 : Set value
        #                    3 : Delete value
        #                    4 : Create key
        #                    5 : Delete key }
        
        def doBrowser():
            global filepath
            filepath = filedialog.askopenfilename()
            try:
                file_directory.delete(0,'end')
                file_directory.insert('end', filepath)
                with open(filepath,'r') as file:
                    content = file.read()
                    textBox.delete('1.0','end')
                    textBox.insert('end',content)
                    
            except Exception:
                pass
        def doSendMessenger():
            send(SEND_REG_FILE)
            msg = textBox.get('1.0','end-1c')
            send1(client,msg)

        global current_function
        current_function = 0

        def dataType_switcher(string):
            switcher = {
                'String': 'REG_SZ',
                'Binary': 'REG_BINARY',
                'DWORD' : 'REG_DWORD',
                'QWORD' : 'REG_QWORD',
                'Multi-String' : 'REG_MULTI_SZ',
                'Expandable String' : 'REG_EXPAND_SZ'
            }
            return switcher.get(string)

        def Send():
            NoticeBox.config(state = 'normal')
            NoticeBox.delete('1.0','end')
            # Get key value
            if current_function == 1:
                send(GET_KEY_VALUE)
                path = path_entry.get('1.0','end-1c')
                value = NameValue.get('1.0','end-1c')
                send1(client,path)
                send1(client,value)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                NoticeBox.insert('end',ans)
                NoticeBox.config(state = 'disabled')

            #Set key value
            if current_function == 2:
                send(SET_KEY_VALUE)
                path = path_entry.get('1.0','end-1c')
                value = NameValue.get('1.0','end-1c')
                data = Data.get('1.0','end-1c')
                data_type = DataType.get()
                data_type = dataType_switcher(data_type)
                
                send1(client,path)
                send1(client,value)
                send1(client,data)
                send1(client,data_type)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')

            


            # Delete key value
            if current_function == 3:
                send(DELETE_KEY_VALUE)
                path = path_entry.get('1.0','end-1c')
                value = NameValue.get('1.0','end-1c')
                send1(client,path)
                send1(client,value)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')

            # Create key
            if current_function == 4:
                send(ADD_NEW_KEY)
                path = path_entry.get('1.0','end-1c')
                send1(client,path)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')

            
            # Delete key
            if current_function == 5:
                send(DELETE_KEY)
                path = path_entry.get('1.0','end-1c')
                send1(client,path)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')
        def Delete():
            NoticeBox.config(state = 'normal')
            NoticeBox.delete('1.0','end')
            NoticeBox.config(state = 'disabled')
        def SelectFunction(event):
            
            
            def GetValue():
                global current_function
                current_function = 1
                Data.place_forget()
                DataType.place_forget()
                
                

            def SetValue():
                global current_function
                current_function = 2
                Data.place(x = 170, y = 215, width = 150, height = 20 )
                DataType.place(x = 330, y =215, width = 150, height =20)

            def DltValue():
                global current_function
                current_function = 3
                Data.place_forget()
                DataType.place_forget()

            def CreateKey(): 
                global current_function
                current_function = 4   
                NameValue.place_forget()
                Data.place_forget()
                DataType.place_forget()
            def DltKey():
                global current_function
                current_function = 5
                pass
            
            s= FunctionChoosen.get()
            if  s == " Set value": SetValue()
            if  s == " Get value": GetValue()
            if  s == " Delete value": DltValue()
            if  s == " Create key": CreateKey()
            if  s == " Delete key": DltKey()
            


        RootFR = Toplevel(Client_windows)
        RootFR.title(55*" "+"Fix Keystroke")
        RootFR.grab_set()
        RootFR.geometry("500x420")

        #Browser---------------
        file_directory = Entry(RootFR)
        file_directory.place(x = 10, y = 10, width = 370)
        file_directory.insert('end', 'Path...')

        Button_Browser = Button(RootFR, text = "Browser", command= doBrowser)
        Button_Browser.place(x = 390, y = 10, width = 100)
        

        #SendMessage-----------
        textBox = Text(RootFR)
        textBox.place(x = 10, y = 40, width = 370, height = 100)
        textBox.insert('end', "Message")
        
        Button_SendMessage = Button(RootFR, text = "Send Message", command= doSendMessenger)
        Button_SendMessage.place(x = 390, y = 40, width = 100, height = 100)

        #Fix------------------
        Label_Fix = Label(RootFR, text  = "Fix Value " + 85*'-')
        Label_Fix.place(x = 10, y = 145)

        #ChooseFunction
        FunctionChoosen = ttk.Combobox(RootFR,state="readonly")
        FunctionChoosen.set("Select function") 
        FunctionChoosen['values'] = (' Get value',' Set value',' Delete value',' Create key', ' Delete key')
        FunctionChoosen.place(x = 10, y =165, width = 477)
        FunctionChoosen.bind('<<ComboboxSelected>>', SelectFunction)

        #Path
        path_entry = Text(RootFR)
        path_entry.place(x = 10, y = 190, width = 477, height = 20)
        path_entry.insert('end', "Path")

        

        #NoticeBox
        NoticeBox = Text(RootFR,state = 'disabled')

        NoticeBox.place(x = 10, y = 240, width = 477, height = 100)

        #NameValue
        NameValue = Text(RootFR)
        NameValue.place(x = 10, y = 215, width = 150, height = 20)
        NameValue.insert('end', "Name Value")

        #Value
        Data = Text(RootFR)
        Data.place(x = 170, y = 215, width = 150, height = 20)
        Data.insert('end', "Data")

        #ChooseType
        DataType = ttk.Combobox(RootFR,state="readonly")
        DataType.set("Select Value Type") 
        DataType['values'] = ('String','Binary','DWORD','QWORD', 'Multi-String', 'Expandable String')
        DataType.place(x = 330, y =215, width = 150, height =20)
        DataType.bind('<<ComboboxSelected>>', SelectFunction)

        #Send, delete button
        Button_Send = Button(RootFR, text = 'Send', command=Send)
        Button_Send.place (x = 110, y = 360, width = 100)

        Button_Delete = Button(RootFR, text = 'Delete', command= Delete)
        Button_Delete.place (x = 280, y = 360, width = 100) 
    else:
        mbox.showinfo(None,"No connection established!")


# CONNECT TO SERVER------------------------------------------------
def connect():
    global connected
    IP_server = InputField.get()
    address = (IP_server,PORT)
    try:
        client.connect(address)
        connected = True
        mbox.showinfo(None,f"Connection establish!\n Server IP: {IP_server}")
    except Exception:
        connected =False
        print(Exception)
        mbox.showinfo(None,"Server not found.")

# EXIT == DISCONNECT FROM SERVER------------------------------------
def exit(): 
    try:
        send(DISCONNECT_MESSAGE)
    except Exception as e:
        print(e)
    Client_windows.destroy()
    
# Take screenshot
def doTakeScreenshot():
    global connected
    if connected == True:

        send(TAKE_SCREEN_SHOT)
        recv_file1(client,"ServerScreenShot.png")
        im = Image.open("ServerScreenShot.png")
        im.show()
    else:
        mbox.showinfo(None,"No connection established!")

# Shutdown

def doShutDown():
    global connected
    if connected == True:

        send(SHUTDOWN)
        info = recv1(client)
        mbox.showinfo(None,info)
    else:
        mbox.showinfo(None,"No connection established!")
        







#INIT WINDOW
Client_windows = Tk()
Client_windows.title(80*" "+TITLE)
Client_windows.geometry("600x400")

#Create buttons
InputField = Entry(Client_windows,width = 50)
InputField.place(x = 100,y=50)


Connect_button = Button(Client_windows,text = "Connect",padx =25, pady=1, command= connect)
Connect_button.place(x = 440, y = 50)

ProcessRunning_button = Button(Client_windows, text = "Process Running", padx = 10, pady = 120, command= doProcessRunning)
ProcessRunning_button.place(x =54, y =100)

AppRunning_button = Button(Client_windows, text = "App Running", padx = 80, pady = 30, command= doAPPRunning)
AppRunning_button.place(x =184, y =100)

Shutdown_button =  Button(Client_windows, text = "Shutdown", padx = 20, pady = 23, command= doShutDown)
Shutdown_button.place(x =184, y =200)

ScreenShot_button =  Button(Client_windows, text = "PrintScreen", padx = 31, pady = 23, command= doTakeScreenshot)
ScreenShot_button.place(x =289, y =200)

Keystroke_button = Button(Client_windows, text = "Keystroke", padx =25, pady =53, command= doKEYSTROKE)
Keystroke_button.place(x = 437, y = 100)

RegistryOverwrite_button = Button(Client_windows, text = "Fix Registry", padx = 82, pady = 30, command= doFixRegistry)
RegistryOverwrite_button.place(x = 184, y = 279)

Exit_button = Button(Client_windows, text="Exit", padx =40, pady = 47, command= exit)
Exit_button.place(x = 437, y =245)

Client_windows.mainloop()

