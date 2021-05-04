import wmi
 


def find_process_name( id_to_find):
    f=wmi.WMI()

    for process in f.Win32_Process():
        if process.ProcessId == id_to_find:
            return process.Name

def check_running_process():
    f=wmi.WMI()

    print("pid   Process name")
    for process in f.Win32_Process():
        print(f"{process.ProcessId:<10} {process.Name}")






def kill_process_by_id(process_id):
    f=wmi.WMI()
    cnt = 0
    
    for process in f.Win32_Process():
        if process.ProcessId == process_id:
            process.Terminate()
            cnt+= 1 
    if cnt == 0:
        return False
    else:
        return True

def kill_process_by_name(process_name):
    f=wmi.WMI()
    cnt = 0
    for process in f.Win32_Process():
        if process.Name == process_name:
            process.Terminate()
            cnt+= 1 
    if cnt == 0:
        return False
    else:
        return True








