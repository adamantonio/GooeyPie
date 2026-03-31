import sys
if sys.platform == 'win32':
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International")
        value, regtype = winreg.QueryValueEx(key, "sShortDate")
        print("winreg format:", value)
    except Exception as e:
        print("error", e)
