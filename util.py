import win32gui,win32ui,win32con,win32api,win32print
from PIL import Image
# 获取权限
from ctypes import windll,wintypes,byref,sizeof
from sys import exit
import socket,json
from time import sleep
from random import randint
from numpy import array
from os import system
import config

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

def help(actions:list):
    print('1. 更新本地对比图片')
    print('2. 获取屏幕位置信息')
    for i in range(len(actions)):
        print(str(i+3) + '. ' + actions[i])
    print('0. 退出')

def update():
    version_fd = open('./version','r')
    version = version_fd.read()
    version_fd.close()
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect(('code.xibai.xyz',33333))
        s.send(b'update\n')
        new_version = s.recv(1000)
        new_version = new_version.decode()
        if version.strip() != new_version.strip():
            print('new version: ',new_version)
            choose = input("检测到新版本，是否选择升级（y/n）：")
            if choose.lower() == 'y':
                system('.\\update.exe')
                exit()
            elif choose.lower() == 'n':
                pass
            else:
                print('非法输入，默认放弃升级')
    except Exception as e:
        print(e)
        print('检测新版本失败，默认运行现有版本')
    s.close()

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
 
def get_system_dpi(window_hwnd):
    """获取缩放后的分辨率"""
    #windll.shcore.SetProcessDpiAwareness(0)
    
    hdc = win32gui.GetDC(window_hwnd)
    a = wintypes.DWORD()
    windll.shcore.GetProcessDpiAwareness(window_hwnd,byref(a))
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
    temp.append(hwnd)
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    temp.append((left, top, right, bottom))
    windows[hwnd] = temp
  
def check_windows(window_name:str):
    windows = {} ; length = 0
    dst = []
    win32gui.EnumWindows(_callback, windows)
    # print("Enumerated a total of  windows with %d classes"%(len(windows)))
    for item in windows:
        if window_name == windows[item][2] and window_name != "":
            dst.append(windows[item])
            length += 1
    
    if length == 0:
        print(window_name+" is notfound")
        return False,dst
    
    return True,dst


def check_user(user_name:str):
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect(('code.xibai.xyz',33333))
        s.send(b'user\n')
        name_list = s.recv(1500).decode('utf-8')
        s.close()
        for i in name_list.split('\n'):
            if user_name == i:
                return True
        return False
    except Exception as e:
        print(e)
        print('用户信息查询失败，姑且当你是自己人，继续运行')
        return True

def init_window_pos(window_hwnd,x,y):
    try:
        win32gui.SetWindowPos(window_hwnd, win32con.HWND_NOTOPMOST, 0, 0, x, y, win32con.SWP_SHOWWINDOW)#win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
        sleep(0.5)
    except Exception as e:
        print("init_window_pos error",e)
        error_exit()

if __name__=="__main__":
    a=get_system_dpi('')
    print(a)
    check_windows("阴阳师-网易游戏")
    #print(win32process.GetWindowThreadProcessId(131592))

def mouse_click(window_hwnd,x,y):
    try:
        x += config.chang_x//2
        tmp_y = config.chang_y+(35/config.sys_dpi)
        y += int(tmp_y//2)
        if config.mode_flag % 2 == 1:
            print(x,y)
        win32api.SendMessage(window_hwnd,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
        win32api.SendMessage(window_hwnd,win32con.WM_LBUTTONUP,0,(y << 16)+x)
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
def get_windows(window_hwnd,flag) -> Image.Image|None:
    try:
        # time.sleep(0.3)
        # pythoncom.CoInitialize()
        # shell = win32com.client.Dispatch("WScript.Shell")
        # shell.SendKeys('%')
        # # 将窗口放在前台，并激活该窗口（窗口不能最小化）
        # #win32gui.SetForegroundWindow(window_hwnd)
        # time.sleep(0.3)
        # pythoncom.CoInitialize()
        # shell = win32com.client.Dispatch("WScript.Shell")
        # shell.SendKeys('%')
        
        # 获取窗口DC
        window_hdDC = win32gui.GetWindowDC(window_hwnd)
        
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
                wintypes.HWND(window_hwnd),
                wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                byref(rect),
                sizeof(rect)
            )
            width,height = rect.right - rect.left - 2, rect.bottom - rect.top - 45 - 2
        else:      
            width,height = (0,0)

        left, top, right, bottom = win32gui.GetWindowRect(window_hwnd)
        if flag % 2 == 1:
            print("\n实际屏幕显示位置",rect.left, rect.top,rect.right , rect.bottom)
            print("系统记录位置",left, top, right, bottom)
        if left < 0 or top < 0:
            print("\n实际屏幕显示位置",rect.left, rect.top,rect.right , rect.bottom)
            print("系统记录位置",left, top, right, bottom)
            print("\a\n请把目标窗口打开至桌面（不能最小化）")

        # 根据句柄创建一个DC
        newhdDC = win32ui.CreateDCFromHandle(window_hdDC)
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
        win32gui.ReleaseDC(window_hwnd,window_hdDC)

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

def get_img_pixel_list(img:Image.Image,check_area:list):
    img_pixel_list = []
    x,y = img.size
    x_1 = int(x * check_area[0])
    x_2 = int(x * check_area[1])
    y_1 = int(y * check_area[2])
    y_2 = int(y * check_area[3])
    x = 0 ; sum_x = (x_2 - x_1)/9
    while x < x_2:
        if x == 0:
            x = x_1
        y = 0 ; sum_y = (y_2-y_1)/9
        while y < y_2:
            if y == 0:
                y = y_1
            img_pixel_list.append(img.getpixel((x,y)))
            y += sum_y
        x += sum_x
    return img_pixel_list

def get_pixel_feature(pixel_list:list):
    tmp_pixel = [0,0,0]
    for i in pixel_list:
        tmp_pixel[0] += i[0]
        tmp_pixel[1] += i[1]
        tmp_pixel[2] += i[2]
    tmp_len = len(pixel_list)
    tmp_pixel[0] //= tmp_len
    tmp_pixel[1] //= tmp_len
    tmp_pixel[2] //= tmp_len
    return tmp_pixel

def identify(dst_pixel_list, tmp_img:Image.Image, check_area:list, check_pos:list):
    pixel_sum = [0,0,0]
    # 预设画面：img_pixel
    # 实时画面色彩特征获取：tmp_pixel_list
    tmp_pixel_list = get_img_pixel_list(tmp_img,check_area) if len(check_pos) == 0 else get_img_pixel_list(tmp_img,check_pos)
    # tmp_pixel = get_pixel_feature(tmp_pixel_list)
    tmp_len = len(tmp_pixel_list)
    for i in range(tmp_len):
        pixel_sum[0] += abs(tmp_pixel_list[i][0] - dst_pixel_list[i][0])
        pixel_sum[1] += abs(tmp_pixel_list[i][1] - dst_pixel_list[i][1])
        pixel_sum[2] += abs(tmp_pixel_list[i][2] - dst_pixel_list[i][2])
    pixel_sum[0] /= tmp_len
    pixel_sum[1] /= tmp_len
    pixel_sum[2] /= tmp_len
    # 判断颜色近似度
    if config.mode_flag %2 ==1:
        print(pixel_sum)
    if pixel_sum[0] <= 10 and pixel_sum[0] >= 0 and pixel_sum[1] <= 10 and pixel_sum[1] >= 0 and pixel_sum[2] <= 10 and pixel_sum[2] >= 0:
        return True
    else:
        return False

def action(action:dict):
    count = 0
    while True:
        count = input("准备刷多少次？")
        if count.isdigit():
            count = int(count)
            break
    dst_pixel_list = {}
    for i in action:
        tmp_pixel_list = get_img_pixel_list(Image.open(action[i]["img_path"]),action[i]["check_area"]) if len(action[i]["check_pos"]) == 0 else get_img_pixel_list(Image.open(action[i]["img_path"]),action[i]["check_pos"])
        dst_pixel_list[i] = tmp_pixel_list#get_pixel_feature(tmp_pixel_list)

    flag = 0
    while count > 0:
        
        window = get_windows(config.yys_window_hwnd,config.mode_flag)
        for i in action:
            if identify(dst_pixel_list[i],window,action[i]["check_area"],action[i]["check_pos"]):
                print("\r"+action[i]["message"]+"                           ",end='')
                if action[i]["type"] == 0:
                    flag = 0
                elif action[i]["type"] == 1:
                    if flag == 0:
                        count -= 1
                        flag = 1
                if len(action[i]["click_area"]) == 0:
                    continue
                # 1480-1540 / 1579   762-820 / 887
                x_left,x_right,y_left,y_right = action[i]["click_area"]
                x=rand_num(int(x_left * config.init_x),int(x_right * config.init_x))
                y=rand_num(int(y_left * config.init_y),int(y_right * config.init_y))
                
                if config.mode_flag % 2 == 1:
                    print("\n点击位置：",x,y)
                mouse_click(config.yys_window_hwnd,int(x),int(y))
                sleep(0.3)