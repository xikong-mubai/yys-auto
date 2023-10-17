import win32process,win32api,win32con
from ctypes import windll
import requests,zipfile

def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print('\r\n',e)
        return False

print("admin: ",is_admin())

for i in win32process.EnumProcesses():
    try:
        process  = win32api.OpenProcess(
                        win32con.PROCESS_ALL_ACCESS,
                        #win32con.PROCESS_QUERY_INFORMATION|win32con.PROCESS_VM_READ,
                        False,
                        i
                    )
        for j in win32process.EnumProcessModules(process):
            tmp_name = win32process.GetModuleFileNameEx(process,j)
            if 'yys.exe' in tmp_name:
                print(i,j,tmp_name)
                win32process.TerminateProcess(process,0)
    except Exception as e:
        #print(i,e)
        pass

url = 'https://code.xibai.xyz/yys-auto.zip'
r = requests.get(url,verify=False)
yys_zip = open('./yys-auto.zip','wb')
yys_zip.write(r.content)
yys_zip.close()

yys_zip_fd = zipfile.ZipFile('./yys-auto.zip')
yys_zip_fd.extractall()
