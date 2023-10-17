import win32process,win32api,win32con

for i in win32process.EnumProcesses():
    if i != 32852 and i != 22940:
        continue
    try:
        process  = win32api.OpenProcess(
                        win32con.PROCESS_ALL_ACCESS,
                        #win32con.PROCESS_QUERY_INFORMATION|win32con.PROCESS_VM_READ,
                        False,
                        i
                    )
        for j in win32process.EnumProcessModules(process):
            tmp_name = win32process.GetModuleFileNameEx(process,j)
            print(i,j,tmp_name)
    except Exception as e:
        #print(i,e)
        pass