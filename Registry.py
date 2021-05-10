import winreg

sHKEY_CURRENT_USER = "HKEY_CURRENT_USER"

def get_registry_value(path, name = "", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        try:
            start_key = getattr(winreg, path[0])
        except AttributeError:
            return "Invalid path!"
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
                while not desc or desc[0]!= name:
                    desc = winreg.EnumValue(handle,i)
                    i += 1
                return desc[1]
    except FileNotFoundError:
        return "Invalid path!"

OneDrive = get_registry_value(r"HKEY_CURRENT_USER\Environment","OneDrive")
print(OneDrive)
