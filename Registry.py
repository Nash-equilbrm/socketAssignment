import winreg
import os

def HKeyAttribute(key):
    switcher = {
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
    }
    return switcher.get(key)
     
def getKeyFromPath(path):
    Slash = path.find('\\')
    hkey = ""
    sub_key = ""

    key = path[:Slash]

    sub_key = path[Slash + 1:]

    hkey = HKeyAttribute(key)

    return hkey, sub_key




def get_registry_value(path, name = "", start_key = None):
    # print(path)
    # print(name)
    # print(start_key)
    # print('\n')
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        try:
            start_key = getattr(winreg, path[0])
        except AttributeError:
            return "ERROR: INVALID PATH"
        return get_registry_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    try:
        with winreg.OpenKey(start_key, subkey) as handle:
            assert handle, "Cannot open wanted key"
            if path:
                return get_registry_value(path, name, handle)
            else:
                desc, i = None, 0
                try:
                    while not desc or desc[0]!= name:
                        desc = winreg.EnumValue(handle,i)
                        i += 1
                    return desc[1]
                except OSError:
                    return "ERROR: INVALID PATH"
    except FileNotFoundError:
        return "ERROR: INVALID PATH"



# OneDrive = get_registry_value(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System","shutdownwithoutlogon")
# print(OneDrive)
# p = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\new_key"




