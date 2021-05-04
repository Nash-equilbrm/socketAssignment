import sys
import socket
import threading
import time
from ScreenShot import*
from RunningProccess import*

HEADER = 64
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR= (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT!"
TAKE_SCREEN_SHOT = "TAKE SCREENSHOT"
RUNNING_PROCESS ="CHECK RUNNING PROCESS"
STOP_LISTING = "STOP LISTING"
KILL_PROCESS_VIA_PID = "KILL PROCESS VIA PID"
KILL_PROCESS_VIA_PID_V2 = "KILL PROCESS VIA PID V2"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def conn_send(conn,send_this):
    conn.send(send_this.encode(FORMAT))
def conn_recv(conn):
    return conn.recv(1024).decode(FORMAT)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}") 
            reply=""


            if msg == TAKE_SCREEN_SHOT:
                Take_Screenshot("ScreenShot.png")
                reply +="SREENSHOT TAKEN."


            elif msg == RUNNING_PROCESS:
                obj = wmi.WMI()
                print("pid   Process name")
                conn.send("pid   Process name".encode(FORMAT))
                for process in obj.Win32_Process():
                    print(f"{process.ProcessId:<10} {process.Name}")
                    conn.send(f"{process.ProcessId:<10} {process.Name}".encode(FORMAT))
                conn.send(STOP_LISTING.encode(FORMAT))
                reply +="PROCCESS LISTED"



            elif msg == KILL_PROCESS_VIA_PID:
                conn.send("Deleting process with PID: ".encode(FORMAT))
                pid = conn.recv(1024).decode(FORMAT)
                pid = int(pid)
                process_killed = kill_process_by_id(pid)
                if process_killed == True:
                    reply += f"PROCESS ID: {pid} TERMINATED"
                else:
                    reply += f"PROCESS ID: {pid} NOT FOUND"

            elif msg == KILL_PROCESS_VIA_PID_V2:
                conn.send("Deleting process with PID: ".encode(FORMAT))
                pid = conn.recv(1024).decode(FORMAT)
                pid = int(pid)
                f=wmi.WMI()
                cnt = 0
                
                for process in f.Win32_Process():
                    if process.ProcessId == pid:
                        process.Terminate()
                        cnt+= 1 
                if cnt == 0:
                    reply += f"PROCESS ID: {pid} NOT FOUND"
                else:
                    reply += f"PROCESS ID: {pid} TERMINATED"

               
                


            elif msg == DISCONNECT_MESSAGE:
                reply +="CONNECTION TERMINATED!"
                connected = False
            else:
                reply += "MESSAGE RECEIVED."
            time.sleep(0.500)
            conn.send(reply.encode(FORMAT))
            #print(f"[{addr}] {msg}")    
            
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args= (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


    
print("[STARTING] server is starting ...")
start()
