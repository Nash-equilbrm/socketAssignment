import sys
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
DISCONNECT_MESSAGE = "DISCONNECT!"
TAKE_SCREEN_SHOT = "TAKE SCREENSHOT"
RUNNING_PROCESS ="CHECK RUNNING PROCESS"
STOP_LISTING = "STOP LISTING"
KILL_PROCESS_VIA_PID = "KILL PROCESS VIA PID"
KILL_PROCESS_VIA_PID_V2 = "KILL PROCESS VIA PID V2"



client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
   
    #print(client.recv(1024).decode(FORMAT))


def Execute():
    while True:
        msg = input()
        send(msg)
        if msg == RUNNING_PROCESS:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
            while True:
                receiving_msg = client.recv(1024).decode(FORMAT)
                if receiving_msg == STOP_LISTING:
                    break
                print(receiving_msg)
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
        elif msg == TAKE_SCREEN_SHOT:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)

        elif msg == DISCONNECT_MESSAGE:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
            break
        elif msg == KILL_PROCESS_VIA_PID:                        
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
            pid = input()
            client.send(pid.encode(FORMAT))


            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
           

        elif msg == KILL_PROCESS_VIA_PID_V2:                        
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
            pid = input()
            client.send(pid.encode(FORMAT))


            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
           
        else:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(receiving_msg)
        

        
    sys.exit()

Execute()
