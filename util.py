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

def identify(message:str, dst_img:Image.Image, tmp_img:Image.Image, area:dict, pos:list):
    pixel_sum = [0,0,0]
    # 预设画面：img_pixel
    dst_img_pos_list = []
    x,y = dst_img.size
    x_1 = int(x * area["x_1"])
    x_2 = int(x * area["x_2"])
    y_1 = int(y * area["y_1"])
    y_2 = int(y * area["y_2"])
    for i in range(x_1, x_2, x_2 - x_1):
        for j in range(y_1, y_2, y_2 - y_1):
            dst_img_pos_list.append(dst_img.getpixel((i,j)))
    # 实时画面色彩特征获取：tmp_pixel_list
    tmp_pixel_list = []
    x,y = tmp_img.size
    x_1 = int(x * area["x_1"])
    x_2 = int(x * area["x_2"])
    y_1 = int(y * area["y_1"])
    y_2 = int(y * area["y_2"])
    for i in range(x_1, x_2, x_2 - x_1):
        for j in range(y_1, y_2, y_2 - y_1):
            tmp_pixel_list.append(tmp_img.getpixel((i,j)))        
    length = min(len(tmp_pixel_list),len(dst_img_pos_list))
    for i in range(length):
        pixel_sum[0] += abs(tmp_pixel_list[i][0] - dst_img_pos_list[i][0])
        pixel_sum[1] += abs(tmp_pixel_list[i][1] - dst_img_pos_list[i][1])
        pixel_sum[2] += abs(tmp_pixel_list[i][2] - dst_img_pos_list[i][2])
    # 判断颜色近似度
    if abs(pixel_sum[0] / length) < 10 and abs(pixel_sum[1] / length) < 10 and abs(pixel_sum[2] / length) < 10:
        message = '\r'+message+' '*20
        print("\r"+message)
        return True
    else:
        return False

def action(action:dict):
    count = input("准备刷多少次？")

############################################################ 肝到这里了，该计算次数了，完事处理单次活动的各个动作识别处理

    for i in choose:
    i = ord(i)
    result *= 10
    result += i - 48
    if i < 48 or i > 57:
        print('对叭起, 我不认识它QAQ')
        break
    for i in action:
        dst_img = Image.open(action[i]["img_path"])
        window = get_windows(yys_window_hwnd,flag)


        # 开始按钮：  1503/1579  790/887
        tmp_pixel_list = tmp_img.getpixel((int(0.95 * x),int(0.8901 * y)))
        # 体力消耗标识：  1464/1579  807-826 /887
        wait_button_pixel_1 = tmp_img.getpixel((int(0.92717 * x),int(0.92108 * y)))
        wait_button_pixel_2 = room_member_img.getpixel((int(0.92717 * img_x),int(0.92108 * img_y)))
        wait_button_pixel = [
            wait_button_pixel_1[0] - wait_button_pixel_2[0],
            wait_button_pixel_1[1] - wait_button_pixel_2[1],
            wait_button_pixel_1[2] - wait_button_pixel_2[2]
        ]
        if tmp_pixel_list[0] == tmp_pixel_list[1] and tmp_pixel_list[1] == tmp_pixel_list[2]:
            print("\r等待成员中            ",end='')

        elif abs(wait_button_pixel[0]) < 5 and abs(wait_button_pixel[1]) < 5 and abs(wait_button_pixel[2]) < 5:
            print("\r等待房主中            ",end='')

        else:
            # 1480-1540 / 1579   762-820 / 887
            x=rand_num(int(0.9373 * init_x),int(0.9653 * init_x))
            y=rand_num(int(0.8791 * init_y),int(0.91446 * init_y))
            
            if flag % 2 == 1:
                print("\n点击位置：",x,y)
            mouse_click(yys_window_hwnd,int(x),int(y))
            print("\r开始                        ",end='')
            sleep(0.3)