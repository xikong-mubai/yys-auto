import ctypes,os
from time import sleep
from numpy import ctypeslib,array

# 添加 DLL 目录到 PATH
#DLL_PATH = "windows-capture.dll"
DLL_PATH = "./windows-capture.dll"
#os.environ["PATH"] = os.path.dirname(DLL_PATH) + ";" + os.environ["PATH"]
# 加载 DLL
#dll = ctypes.WinDLL(DLL_PATH)
dll = ctypes.cdll.LoadLibrary(DLL_PATH)

init_capture = dll.init_capture
#update_frame= dll.update_frame
get_frame = dll.get_frame
stop_capture = dll.stop_capture

init_capture.argtypes = [ctypes.c_void_p]
get_frame.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int,
                      ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                      ctypes.POINTER(ctypes.c_uint64)]
get_frame.restype = ctypes.c_bool
#update_frame.restype = ctypes.c_bool

import win32gui,win32ui,win32con,win32api,win32print,win32process
def get_system_dpi(window_hwnd):
    """获取缩放后的分辨率"""
    # 尝试设置程序dpi比例，不可行  ctypes.windll.shcore.SetProcessDpiAwareness(0)
    # PROCESS_DPI_AWARENESS = {
    #     "PROCESS_DPI_UNAWARE" : 0,          # DPI 不知道。 此应用不会缩放 DPI 更改，并且始终假定其比例系数为 100% (96 DPI) 。 系统将在任何其他 DPI 设置上自动缩放它。
    #     "PROCESS_SYSTEM_DPI_AWARE" : 1,     # 系统 DPI 感知。 此应用不会缩放 DPI 更改。 它将查询 DPI 一次，并在应用的生存期内使用该值。 如果 DPI 发生更改，应用将不会调整为新的 DPI 值。 当 DPI 与系统值发生更改时，系统会自动纵向扩展或缩减它。
    #     "PROCESS_PER_MONITOR_DPI_AWARE" : 2 # 按显示器 DPI 感知。 此应用在创建 DPI 时检查 DPI，并在 DPI 发生更改时调整比例系数。 系统不会自动缩放这些应用程序。 
    # }
    hdc = win32gui.GetDC(window_hwnd)
    a = ctypes.wintypes.DWORD()
    ctypes.windll.shcore.GetProcessDpiAwareness(window_hwnd,ctypes.byref(a))
    if a.value == 0:
        dpi = float(win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hdc, win32con.HORZRES))
        # print(win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES),win32print.GetDeviceCaps(hdc, win32con.HORZRES))
    else:
        x_dpi: int = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
        # dpi:screen_scale_rate = x_dpi/96
        dpi = float(x_dpi / 96)
    a = -1 if a.value == 4294967295 else a.value
    return dpi,float(a)

def init_window_pos(window_hwnd,x,y):
    try:
        win32gui.SetWindowPos(window_hwnd, win32con.HWND_NOTOPMOST, 0, 0, x, y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
        sleep(0.5)
    except Exception as e:
        print("init_window_pos error",e)
        input("输入任意键退出")
        exit()

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

def check_windows():
    windows = {} ; length = 0
    dst = []
    win32gui.EnumWindows(_callback, windows)
    # print("Enumerated a total of  windows with %d classes"%(len(windows)))
    for item in windows:
        # if window_name == windows[item][2] and window_name != "":
        dst.append(windows[item])
        length += 1
    if length == 0:
        print("Not found any window what have title.")
        return False,dst
    return True,dst

def check_child_windows(win_handle):
    windows = {} ; length = 0 ; dst = []
    win32gui.EnumChildWindows(win_handle,_callback, windows)
    for item in windows:
        if 'MuMuPlayer' == windows[item][2]:
            dst.append(windows[item])
            length += 1
    if length == 0:
        print("MuMuPlayer is notfound")
        return False,dst
    return True,dst

def get_hwnds_from_pid(pid = None):
    if pid == None or not isinstance(pid,int) or pid < 0:
        return False,[]
    def callback(hwnd, hwnds):
        print(hwnd)
        _, result = win32process.GetWindowThreadProcessId(hwnd)
        print('    ',_, result)
        if result == pid or _ == pid:
            hwnds.append(hwnd)
            return 
        win32gui.EnumChildWindows(hwnd,callback,hwnds)
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return True,hwnds 

def init_capture_handle(hwnd):
    hwnd = ctypes.c_void_p(hwnd)
    init_capture(hwnd)

# 接收帧数据
buffer = (ctypes.c_uint8 * (1920*1080*3))()
BUFFER_SIZE = 1920*1080*3
width = ctypes.c_int()
height = ctypes.c_int()
out_frame_id = ctypes.c_uint64()

import threading
frame_ready = threading.Event()
# 定义回调类型：__stdcall(void)
CALLBACK_TYPE = ctypes.WINFUNCTYPE(None)
# 定义 Python 回调函数
@CALLBACK_TYPE
def on_new_frame():
    # print("New frame arrived!")
    frame_ready.set()
    # 可以在这里设置事件或触发 UI 刷新
# 注册回调函数到 DLL
dll.register_frame_callback(on_new_frame)

from PIL import Image
# 获取阴阳师运行状态
def get_windows() -> Image.Image|None:
    # 检查是否有新帧
    if frame_ready.is_set():
        frame_ready.clear()
        try:
            if get_frame(buffer, BUFFER_SIZE, ctypes.byref(width), ctypes.byref(height), ctypes.byref(out_frame_id)):
                try:
                    img_array = ctypeslib.as_array(buffer, shape=(width.value * height.value * 3,))
                    img_array = img_array[:width.value * height.value * 3]  # 截取有效数据
                    img_array = img_array.reshape((height.value, width.value, 3))
                    img = Image.fromarray(img_array, 'RGB')
                    sleep(0.005)
                    return img
                except Exception as e:
                    print("Image decode error:", e)
        except Exception as error:
            print("\r\nget_window error!!!\n",error)
    return None

import atexit
def exit_stop():
    stop_capture()
atexit.register(exit_stop)