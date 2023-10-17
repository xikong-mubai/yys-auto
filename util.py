import win32gui,win32ui,win32con,win32api,win32print,win32process
from PIL import Image
# 获取权限
from ctypes import windll,wintypes,byref,sizeof
from sys import exit
import socket
from time import sleep
from random import randint
from numpy import array

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

def help():
    print('1. 魂土')
    print('2. 御灵')
    print('4. 更新本地对比图片')
    print('5. 获取屏幕位置信息')
    print('0. 退出')

def error_exit():
    input("输入任意键退出")
    exit()

def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print('\r\n',e)
        return False

# 生成随机数
def rand_num(x:int, y:int):
    return round(randint(x, y),3)
 
def get_system_dpi(window_name):
    """获取缩放后的分辨率"""
    #windll.shcore.SetProcessDpiAwareness(0)
    if window_name == '':
        hdwn = 0
    else:
        hdwn = win32gui.FindWindow(None,window_name)
    hdc = win32gui.GetDC(hdwn)
    a = wintypes.DWORD()
    windll.shcore.GetProcessDpiAwareness(hdwn,byref(a))
    if a.value == 0:
        dpi = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hdc, win32con.HORZRES)
    else:
        x_dpi: int = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
        dpi = x_dpi / 96
    #screen_scale_rate=x_dpi#/96
    
    a = -1 if a.value == 4294967295 else a.value
    return dpi,a

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
        if window_name == windows[item][2] and window_name != "":
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
        sleep(0.5)
    except Exception as e:
        print("init_window_pos error",e)
        error_exit()

if __name__=="__main__":
    a=get_system_dpi('')
    print(a)
    check_windows("阴阳师")
    #print(win32process.GetWindowThreadProcessId(131592))

def mouse_click(windowsname,x,y):
    try:
        handle = win32gui.FindWindow(None,windowsname)
        win32api.SendMessage(handle,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
        win32api.SendMessage(handle,win32con.WM_LBUTTONUP,0,(y << 16)+x)
    except Exception as e:
        print(e)

    sleep(0.1)
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
def get_windows(windowsname,flag) -> Image.Image|None:
    try:
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
            print("\r\nDwmGetWindowAttributeError")
        if f: # Vista & 7 stuff
            rect = wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(  
                wintypes.HWND(yys_handle),
                wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                byref(rect),
                sizeof(rect)
            )
            width,height = rect.right - rect.left - 2, rect.bottom - rect.top - 45 - 2
        else:      
            width,height = (0,0)

        left, top, right, bottom = win32gui.GetWindowRect(yys_handle)
        if flag % 2 == 1:
            print("\n实际屏幕显示位置",rect.left, rect.top,rect.right , rect.bottom)
            print("系统记录位置",left, top, right, bottom)
        if left < 0 or top < 0:
            print("\a\n请把目标窗口打开至桌面（不能最小化）")

        # 根据句柄创建一个DC
        newhdDC = win32ui.CreateDCFromHandle(yys_hdDC)
        # 创建一个兼容设备内存的DC
        saveDC = newhdDC.CreateCompatibleDC()
        # 创建bitmap保存图片
        saveBitmap = win32ui.CreateBitmap()

        # bitmap初始化
        saveBitmap.CreateCompatibleBitmap(newhdDC, width, height)
        saveDC.SelectObject(saveBitmap)
        sleep(0.3)
        saveDC.BitBlt((0, 0), (width, height), newhdDC,(11,45+1), win32con.SRCCOPY) #(rect.left+1,rect.top+45+1), win32con.SRCCOPY)#(left, top), win32con.SRCCOPY)
        sleep(0.3)
        info = saveBitmap.GetInfo()
        result = saveBitmap.GetBitmapBits(win32con.DIB_RGB_COLORS)
        win32gui.DeleteObject(saveBitmap.GetHandle())
        saveDC.DeleteDC()
        newhdDC.DeleteDC()
        win32gui.ReleaseDC(yys_handle,yys_hdDC)

        screen =[]
        for i in result:
            if i >= 0:
                screen.append(i)
            else:
                screen.append(256+i)
        screen = array(screen,dtype='uint8')
        img = Image.frombuffer("RGB", (info['bmWidth'], info['bmHeight']), screen, 'raw', 'BGRX', 0, 1)
        return img
    except Exception as error:
        print("\r\nget_window error!!!\n",error)
        return None