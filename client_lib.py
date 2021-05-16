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
STOP_LISTING = "STOP"
START_LISTING = "START LISTING"

KILL_PROCESS_VIA_PID = "KILL PROCESS VIA PID"
KILL_PROCESS_VIA_NAME = "KILL PROCESS VIA NAME"
KEY_LOGGING ="KEY LOG"
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


def send_file(filename):
    with open(filename + ".reg","r") as file:
        client.send(filename.encode(FORMAT))
        content = file.read()
        send(content)



def Execute():
    while True:
        msg = input()
        send(msg)
        if msg == RUNNING_PROCESS:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            while True:
                receiving_msg = client.recv(1024).decode(FORMAT)
                if receiving_msg == STOP_LISTING:
                    break
                print(receiving_msg)
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER]: " + receiving_msg)
        elif msg == TAKE_SCREEN_SHOT:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)

        elif msg == DISCONNECT_MESSAGE:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            break
        elif msg == KILL_PROCESS_VIA_PID:                        
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            pid = input()
            client.send(pid.encode(FORMAT))


            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
        

        elif msg == KILL_PROCESS_VIA_NAME:                        
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            p_name = input()
            client.send(p_name.encode(FORMAT))


            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
        
        elif msg == KEY_LOGGING:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)

        elif msg == SHUTDOWN:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            sec = input()
            client.send(sec.encode(FORMAT))
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)

        elif msg == CANCEL_SHUTDOWN:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)

        elif msg ==SEND_REG_FILE:
            filename = input("Input filename: ")
            try:
                send_file(filename)
                receiving_msg = client.recv(1024).decode(FORMAT)
                print(f"[SERVER] " + receiving_msg)
            except IOError:
                print("FILE NOT FOUND")
                client.send("NO FILE SENT!".encode(FORMAT))
                receiving_msg = client.recv(1024).decode(FORMAT)
                print(f"[SERVER] " + receiving_msg)

        elif msg == GET_KEY_VALUE:
            path = input("Input path: ")
            client.send(path.encode(FORMAT))
            name = input("Input name: ")
            client.send(name.encode(FORMAT))
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
        
        elif msg == ADD_NEW_KEY:
            path = input("Input path: ")
            client.send(path.encode(FORMAT))
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
            
        elif msg == DEL_KEY:
            path = input("Input path: ")
            client.send(path.encode(FORMAT))
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
        else:
            receiving_msg = client.recv(1024).decode(FORMAT)
            print(f"[SERVER] " + receiving_msg)
        

        
    sys.exit()

# Execute()

# if __name__ == '__main__':
#     main()