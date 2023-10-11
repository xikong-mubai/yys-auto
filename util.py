import win32gui,win32ui,win32con,win32com.client,random,win32api,win32print
from PIL import Image
from ctypes import windll
import pyautogui,time,pythoncom
# 获取权限
import ctypes, sys, os

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

def help():
    print('1. 魂土')
    print('2. 御灵')
    print('0. 退出')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(e)
        return False

# 生成随机数
def rand_num(x, y):
    return round(random.uniform(x, y),3)
 
def get_system_dpi():
    """获取缩放后的分辨率"""
    hdc = win32gui.GetDC(win32gui.FindWindow(None,"阴阳师-网易游戏"))
    x_dpi: int = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    screen_scale_rate=x_dpi/96
    return screen_scale_rate
 
if __name__=="__main__":
    a=get_system_dpi()
    print(a)

# 检测 阴阳师 窗口比例是否更新
def check_window(dst: Image):
    img_x,img_y = dst.size

    tmp = Image.open('./123.png')
    tmp_img_x,tmp_img_y = tmp.size
    tmp.close()
    if abs(img_x - tmp_img_x) > 15 or abs(img_y - tmp_img_y) > 7: #img_x != tmp_img_x or img_y != tmp_img_y:
        get_windows(yys_window_name,tempimg_name)
        tmp = Image.open('./123.png')
        tmp_img_x,tmp_img_y = tmp.size
        tmp.close()
        if abs(img_x - tmp_img_x) > 15 or abs(img_y - tmp_img_y) > 7:
            print("please update img's image!")
            print("Press enter to close")
            input()
            exit()

# 获取阴阳师运行状态
def get_windows(windowsname,filename):
    try:
        img = Image.open("img/room_wait.png")
        tmp_img_x,tmp_img_y = img.size
        
        # 获取窗口句柄
        print(win32gui.EnumWindows)
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
        
        # win32gui.EnumWindows
        # 获取窗口DC
        yys_hdDC = win32gui.GetWindowDC(yys_handle)
        print("get window DC")
        
        # 获取窗口的位置信息
        left, top, right, bottom = win32gui.GetWindowRect(yys_handle)
        print(left, top, right, bottom,tmp_img_x,tmp_img_y)
        print()
        if left < 0 or top < 0:
            print("\a请把阴阳师窗口打开至桌面（不能最小化）")
        # 窗口长宽
        width = right - left
        height = bottom - top
        #if width != tmp_img_x or tmp_img_y != height:
        if abs(width - tmp_img_x) > 15 or abs(height - tmp_img_y) > 7:
            # 将窗口放在前台，并激活该窗口（窗口不能最小化）
            #win32gui.SetForegroundWindow(yys_handle)

            # 控制窗口的位置和大小 
            # 参数1：控制的窗体
            # 参数2：大致方位,HWND_TOPMOST上方
            # 参数3：位置x
            # 参数4：位置y
            # 参数5：长度
            # 参数6：宽度
            win32gui.SetWindowPos(yys_handle, win32con.HWND_NOTOPMOST, 0, 0, tmp_img_x, tmp_img_y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
            time.sleep(0.5)
            # 获取窗口的位置信息
            left, top, right, bottom = win32gui.GetWindowRect(yys_handle)
            print(left, top, right, bottom,tmp_img_x,tmp_img_y)
            print()
            # 窗口长宽
            width = right - left
            height = bottom - top
            if abs(width - tmp_img_x) > 15 or abs(height - tmp_img_y) > 7:
                win32gui.SetWindowPos(yys_handle, win32con.HWND_NOTOPMOST, 0, 0, tmp_img_x, tmp_img_y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
                time.sleep(0.5)

        # 根据句柄创建一个DC
        newhdDC = win32ui.CreateDCFromHandle(yys_handle)
        # 创建一个兼容设备内存的DC
        saveDC = newhdDC.CreateCompatibleDC()
        # 创建bitmap保存图片
        saveBitmap = win32ui.CreateBitmap()

        # bitmap初始化
        saveBitmap.CreateCompatibleBitmap(newhdDC, width, height)
        saveDC.SelectObject(saveBitmap)
        time.sleep(0.3)
        saveDC.BitBlt((0, 0), (width, height), newhdDC, (left, top), win32con.SRCCOPY)
        time.sleep(0.3)
        saveBitmap.SaveBitmapFile(saveDC, filename)
        win32gui.DeleteObject(saveBitmap.GetHandle())
        saveDC.DeleteDC()
        newhdDC.DeleteDC()
        win32gui.ReleaseDC(yys_handle,yys_hdDC)
    except Exception as error:
        print("get_window error!!!\n",error)