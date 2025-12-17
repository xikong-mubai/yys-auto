# import win32gui,win32ui,win32con,win32api,win32print,win32process
from multiprocessing import freeze_support
freeze_support()
from PIL import Image

# # 获取权限
# from ctypes import windll,wintypes,byref,sizeof
# from sys import exit

import win32gui,win32con,win32api

from yys_util import get_windows
from yys_windows import check_windows,check_child_windows


yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

def _callback( hwnd, extra ):
    windows = extra
    temp=[]
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #if left == 0 and top == 0 and right < 1280 and right > 640:
    temp.append(hwnd)
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    windows[hwnd] = temp

# {
#     1185348: [1185348, 'Qt5156QWindowIcon', 'MuMuPlayer', (4, 37, 756, 460)],
#     1313104: [1313104, 'nemuwin', 'nemudisplay', (4, 37, 756, 460)]
# }
def _callback( hwnd, extra ):
    windows = extra
    temp=[]
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #if left == 0 and top == 0 and right < 1280 and right > 640:
    temp.append(hwnd)
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    temp.append((left, top, right, bottom))
    if len(temp[2]) > 0 and temp[3][2]-temp[3][0] > 6 and temp[3][3] - temp[3][1] > 6 \
        and win32gui.IsWindowVisible(temp[0]):
        windows[hwnd] = temp

if __name__=="__main__":
    # windll.shcore.SetProcessDpiAwareness(0)
    # a=get_system_dpi(0x0470908)
    # print(a)
    # result,windows = check_windows()
    # for i in windows:
    # print(check_child_windows(527930))
    windows = {} ; length = 0 ; dst = []
    win32gui.EnumChildWindows(460390,_callback, windows)
    print(windows)
    # (754, 490, 1869, 1117)
    # (750, 450, 1873, 1120)
    # (6, 40, 756, 462)  125%
    # (3, 40, 756, 463)  150%
    # (0, 0, 760, 465)

    # (3, 47, 758, 472)  150%
    # (0, 0, 762, 483)   150%

    # (5, 40, 1130, 673) 100%
    # (0, 0, 1136, 677)  100%

    # screen,screeninfo = get_windows("阴阳师-网易游戏",'',1)
    # print(type(screen))
    # print(dir(screen))
    # screen_u = []
    # for i in screen:
    #     if i >= 0:
    #         screen_u.append(i)
    #     else:
    #         screen_u.append(256+i)
    #screen = numpy.array(screen_u,dtype='uint8')
    #screen = numpy.array(screen,dtype='uint8')
    #print(screen)

# 00470908
    # print(hex(windows[0][0]))
    # img = get_windows(windows[0][0])#= Image.frombuffer("RGB", (screeninfo['bmWidth'], screeninfo['bmHeight']), screen, 'raw', 'BGRX', 0, 1)

    # dc = win32gui.GetWindowDC(0x00470908)
    # a = win32gui.GetDlgCtrlID(0x003063A)
    # print(a)
    # windows = {}
    # win32gui.EnumChildWindows(0x0470908,_callback,windows)
    # print(windows)
    # print(win32gui.GetMessage(0x0470908,0,300))
    # print(win32gui.GetDlgItem(0x003063A,a))#.GetClassName(0x00470908))

    # #img = Image.fromarray(screen.astype('uint8')).convert('RGB')
    # img.show()
    # print(img.size)
    # img.close()
    # handle = win32gui.FindWindow(None,"阴阳师-网易游戏")

    # # x,y = 720,440
    # x,y = 1070,625
    # x,y = 730,400

    # import ai_huijuan

    # ai_huijuan.click_xy([5,290,15,310])

    x,y = 200,200
    print("dianji")
    hwnd = 265812
    # win32api.SendMessage(windows[0][0],win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
    # win32api.SendMessage(windows[0][0],win32con.WM_LBUTTONUP,0,(y << 16)+x)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONUP,0,(y << 16)+x)
    import time
    time.sleep(1)
    x,y = 600,206
    print("dianji")
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONUP,0,(y << 16)+x)


    #print(win32process.GetWindowThreadProcessId(131592))
    #init_window_pos(yys_window_name,1180,702)
    #init_window_pos(yys_window_name,753,462)

    # x=rand_num(int(0.87 * img_x),int(0.93 * img_x))
    # y=rand_num(int(0.85 * img_y),int(0.93 * img_y))
    # mouse_click(yys_window_name,x,y)


# class STARTUPINFO(ctypes.Structure):
#     _fields_ = [
#         ("cb", ctypes.c_ulong),          # 结构体的大小
#         ("lpReserved", ctypes.c_wchar_p), # 保留字段
#         ("lpDesktop", ctypes.c_wchar_p),  # 桌面名称
#         ("lpTitle", ctypes.c_wchar_p),    # 标题
#         ("dwX", ctypes.c_ulong),         # X 坐标
#         ("dwY", ctypes.c_ulong),         # Y 坐标
#         ("dwXSize", ctypes.c_ulong),     # X 轴大小
#         ("dwYSize", ctypes.c_ulong),     # Y 轴大小
#         ("dwXCountChars", ctypes.c_ulong),# 字符宽度
#         ("dwYCountChars", ctypes.c_ulong),# 字符高度
#         ("dwFillAttribute", ctypes.c_ulong), # 填充属性
#         ("dwFlags", ctypes.c_ulong),     # 标志
#         ("wShowWindow", ctypes.c_short), # 显示窗口类型
#         ("cbReserved2", ctypes.c_short), # 额外保留字节数
#         ("lpReserved2", ctypes.POINTER(ctypes.c_byte)), # 额外保留字节
#         ("hStdInput", ctypes.c_void_p),  # 标准输入
#         ("hStdOutput", ctypes.c_void_p), # 标准输出
#         ("hStdError", ctypes.c_void_p)   # 标准错误
#     ]

# # 创建进程
# def create_process_as_user():
#     lpExePath = "E:\\happy\\Onmyoji\\Launch.exe"  # 要启动的进程路径
#     # 获取目标进程句柄
#     hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, os.getpid())
#     # 准备启动信息结构体
#     si = win32process.STARTUPINFO()
#     # si.cb = ctypes.sizeof(si)
#     # 初始化进程线程属性列表
#     class PROC_THREAD_ATTRIBUTE_LIST(ctypes.Structure):
#         _fields_ = [("size", ctypes.c_size_t)]
#     # 获取属性列表的大小
#     lpsize = ctypes.c_size_t(0)
#     ctypes.windll.kernel32.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(lpsize))
#     # 创建一个属性列表的缓冲区
#     buffer = ctypes.create_string_buffer(lpsize.value)
#     attribute_list = ctypes.cast(buffer, ctypes.POINTER(PROC_THREAD_ATTRIBUTE_LIST))
#     # 初始化属性列表
#     ctypes.windll.kernel32.InitializeProcThreadAttributeList(attribute_list, 1, 0, ctypes.byref(lpsize))
#     # 设置父进程属性
#     # 将 hProcess 转换为 ctypes.c_void_p 类型
#     hProcess_ctypes = ctypes.c_void_p(int(hProcess))
#     ctypes.windll.kernel32.UpdateProcThreadAttribute(
#         attribute_list, 
#         0, 
#         0x00020000,  # PROC_THREAD_ATTRIBUTE_PARENT_PROCESS
#         ctypes.byref(hProcess_ctypes),
#         ctypes.sizeof(hProcess_ctypes),
#         None,
#         None
#     )
#     # si.lpAttributeList = attribute_list
#     # 创建进程
#     # pi = PROCESS_INFORMATION()
#     success = win32process.CreateProcessAsUser(
#         hToken,  # 用户Token，None表示当前进程
#         lpExePath,  # 可执行路径
#         "",  # 命令行参数
#         None,  # 安全属性
#         None,  # 继承句柄
#         False,  # 是否继承句柄
#         0x00080000 ,  # 启动信息
#         None,  # 环境变量
#         None,  # 当前目录
#         si  # 启动信息结构体
#     )
#     print("Process created with PID:", success)