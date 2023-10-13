import win32gui,win32ui,win32con,win32api,win32print,win32process
# from PIL import Image
# 获取权限
from ctypes import windll,wintypes,byref,sizeof
from sys import exit
import random,time,socket

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

def help():
    print('1. 魂土')
    print('2. 御灵')
    print('0. 退出')

def error_exit():
    input("输入任意键退出")
    exit()

def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(e)
        return False

# 生成随机数
def rand_num(x:int, y:int):
    return round(random.randint(x, y),3)
 
def get_system_dpi():
    """获取缩放后的分辨率"""
    windll.shcore.SetProcessDpiAwareness(1)
    a = wintypes.DWORD()
    windll.shcore.GetProcessDpiAwareness(win32gui.GetDC(win32gui.FindWindow(None,"阴阳师-网易游戏")),byref(a))
    print(a)
    hdc = win32gui.GetDC(win32gui.FindWindow(None,"阴阳师-网易游戏"))
    x_dpi: int = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    print(win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hdc, win32con.HORZRES))
    screen_scale_rate=x_dpi#/96
    return screen_scale_rate

  
def _callback( hwnd, extra ):
    windows = extra
    temp=[]
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #if left == 0 and top == 0 and right < 1280 and right > 640:
    temp.append(hex(hwnd))
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    temp.append((left, top, right, bottom))
    windows[hwnd] = temp
  
def check_windows(window_name:str):
    windows = {}
    win32gui.EnumWindows(_callback, windows)
    # print("Enumerated a total of  windows with %d classes"%(len(windows)))
    for item in windows:
        if windows[item][2] == window_name and window_name != "":
            print(window_name+" confirms existence")
            return True
    print(window_name+" is notfound")
    return False


def check_user(user_name:str):
    s = socket.socket()
    s.connect(('code.xibai.xyz',33333))
    name_list = s.recv(1500).decode('utf-8')
    for i in name_list.split('\n'):
        if user_name == i:
            return True
    return False

def init_window_pos(windowsname,x,y):
    try:
        handle = win32gui.FindWindow(None,windowsname)
        win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, 0, 0, x, y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
        time.sleep(0.5)
    except Exception as e:
        print("init_window_pos error",e)
        error_exit()

if __name__=="__main__":
    a=get_system_dpi()
    print(a)
    check_windows("")
    print(win32process.GetWindowThreadProcessId(131592))
    #init_window_pos(yys_window_name,1180,702)

def mouse_click(windowsname,x,y):
    handle = win32gui.FindWindow(None,windowsname)
    win32api.SendMessage(handle,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
    win32api.SendMessage(handle,win32con.WM_LBUTTONUP,0,(y << 16)+x)


# 检测 阴阳师 窗口比例是否更新
# def check_window(dst: Image):
#     img_x,img_y = dst.size

#     tmp = Image.open('./123.png')
#     tmp_img_x,tmp_img_y = tmp.size
#     tmp.close()
#     if abs(img_x - tmp_img_x) > 15 or abs(img_y - tmp_img_y) > 7: #img_x != tmp_img_x or img_y != tmp_img_y:
#         get_windows(yys_window_name,tempimg_name)
#         tmp = Image.open('./123.png')
#         tmp_img_x,tmp_img_y = tmp.size
#         tmp.close()
#         if abs(img_x - tmp_img_x) > 15 or abs(img_y - tmp_img_y) > 7:
#             print("please update img's image!")
#             print("Press enter to close")
#             input()
#             exit()



# 获取阴阳师运行状态
def get_windows(windowsname,filename):
    try:
        # img = Image.open("img/room_wait.png")
        # tmp_img_x,tmp_img_y = img.size
        # 获取窗口句柄
        # print(win32gui.EnumWindows)
        yys_handle = win32gui.FindWindow(None,windowsname)

        # time.sleep(0.3)
        # pythoncom.CoInitialize()
        # shell = win32com.client.Dispatch("WScript.Shell")
        # shell.SendKeys('%')
        # # 将窗口放在前台，并激活该窗口（窗口不能最小化）
        # #win32gui.SetForegroundWindow(yys_handle)
        # time.sleep(0.3)
        # pythoncom.CoInitialize()
        # shell = win32com.client.Dispatch("WScript.Shell")
        # shell.SendKeys('%')
        
        # 获取窗口DC
        yys_hdDC = win32gui.GetWindowDC(yys_handle)
        
        # 获取窗口的位置信息
        try:
            f = windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
            print("DwmGetWindowAttributeError")
        if f: # Vista & 7 stuff
            rect = wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(wintypes.HWND(yys_handle),
            wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            byref(rect),
            sizeof(rect)
            )
            width,height = rect.right - rect.left, rect.bottom - rect.top - 45
        else:      
            width,height = (0,0)

        left, top, right, bottom = win32gui.GetWindowRect(yys_handle)
        print(rect.left, rect.top,rect.right , rect.bottom)
        print(left, top, right, bottom)
        if left < 0 or top < 0:
            print("\a请把目标窗口打开至桌面（不能最小化）")
        # 窗口长宽
        # width = right - left
        # height = bottom - top
        #if width != tmp_img_x or tmp_img_y != height:
        # if abs(width - tmp_img_x) > 15 or abs(height - tmp_img_y) > 7:
        #     # 将窗口放在前台，并激活该窗口（窗口不能最小化）
        #     #win32gui.SetForegroundWindow(yys_handle)

        #     # 控制窗口的位置和大小 
        #     # 参数1：控制的窗体
        #     # 参数2：大致方位,HWND_TOPMOST上方
        #     # 参数3：位置x
        #     # 参数4：位置y
        #     # 参数5：长度
        #     # 参数6：宽度
        #     win32gui.SetWindowPos(yys_handle, win32con.HWND_NOTOPMOST, 0, 0, tmp_img_x, tmp_img_y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
        #     time.sleep(0.5)
        #     # 获取窗口的位置信息
        #     left, top, right, bottom = win32gui.GetWindowRect(yys_handle)
        #     print(left, top, right, bottom,tmp_img_x,tmp_img_y)
        #     print()
        #     # 窗口长宽
        #     width = right - left
        #     height = bottom - top
        #     if abs(width - tmp_img_x) > 15 or abs(height - tmp_img_y) > 7:
        #         win32gui.SetWindowPos(yys_handle, win32con.HWND_NOTOPMOST, 0, 0, tmp_img_x, tmp_img_y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
        #         time.sleep(0.5)

        # 根据句柄创建一个DC
        newhdDC = win32ui.CreateDCFromHandle(yys_hdDC)
        # 创建一个兼容设备内存的DC
        saveDC = newhdDC.CreateCompatibleDC()
        # 创建bitmap保存图片
        saveBitmap = win32ui.CreateBitmap()

        # bitmap初始化
        saveBitmap.CreateCompatibleBitmap(newhdDC, width, height)
        saveDC.SelectObject(saveBitmap)
        time.sleep(0.3)
        saveDC.BitBlt((0, 0), (width, height), newhdDC, (rect.left,rect.top+45), win32con.SRCCOPY)#(left, top), win32con.SRCCOPY)
        time.sleep(0.3)
        saveBitmap.SaveBitmapFile(saveDC, filename)
        win32gui.DeleteObject(saveBitmap.GetHandle())
        saveDC.DeleteDC()
        newhdDC.DeleteDC()
        win32gui.ReleaseDC(yys_handle,yys_hdDC)
    except Exception as error:
        print("get_window error!!!\n",error)