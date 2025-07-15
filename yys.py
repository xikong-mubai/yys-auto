from sys import version_info,executable,path
print(path)
from yys_util import ctypes
import yys_main
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print('\r\n',e)
        return False

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    if is_admin():
        yys_main.main()
    else:
        if version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
        # else:  # in python2.x
        #     windll.shell32.ShellExecuteW(None, u"runas", unicode(executable), unicode(__file__), None, 1)
        #     pass
