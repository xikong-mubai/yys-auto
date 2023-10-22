# import win32gui,win32ui,win32con,win32api,win32print,win32process
from PIL import Image
# # 获取权限
# from ctypes import windll,wintypes,byref,sizeof
# from sys import exit
# import random,time,socket

import win32gui,win32ui,win32con,win32api,win32print,win32process
#from PIL import Image
from ctypes import windll,wintypes
import ctypes
user32 = windll.user32
gdi32 = windll.gdi32
#import pyautogui,time
# 获取权限
#import random

from util import mouse_click,rand_num,get_system_dpi,check_windows,get_windows

import numpy

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

if __name__=="__main__":
    windll.shcore.SetProcessDpiAwareness(0)
    a=get_system_dpi('')
    print(a)
    check_windows("阴阳师-网易游戏")
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

    img = get_windows("阴阳师-网易游戏",'',1)#= Image.frombuffer("RGB", (screeninfo['bmWidth'], screeninfo['bmHeight']), screen, 'raw', 'BGRX', 0, 1)

    #img = Image.fromarray(screen.astype('uint8')).convert('RGB')
    img.show()
    print(img.size)
    img.close()
    handle = win32gui.FindWindow(None,"阴阳师-网易游戏")

    # x,y = 720,440
    # x,y = 1070,625
    x,y = 730,400
    print("dianji")
    win32api.SendMessage(handle,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
    win32api.SendMessage(handle,win32con.WM_LBUTTONUP,0,(y << 16)+x)


    #print(win32process.GetWindowThreadProcessId(131592))
    #init_window_pos(yys_window_name,1180,702)
    #init_window_pos(yys_window_name,753,462)

    # x=rand_num(int(0.87 * img_x),int(0.93 * img_x))
    # y=rand_num(int(0.85 * img_y),int(0.93 * img_y))
    # mouse_click(yys_window_name,x,y)

# try:
#     f = ctypes.windll.dwmapi.DwmGetWindowAttribute
# except WindowsError:
#     f = None
# if f: # Vista & 7 stuff
#     rect = ctypes.wintypes.RECT()
#     DWMWA_EXTENDED_FRAME_BOUNDS = 9
#     f(ctypes.wintypes.HWND(win32gui.FindWindow(None,'阴阳师-网易游戏')),
#       ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
#       ctypes.byref(rect),
#       ctypes.sizeof(rect)
#       )
#     size = (rect.right - rect.left, rect.bottom - rect.top)        
#     print(dir(rect))
# else:      
#     size = (1)
# print(size)
# print(rect.right , rect.left, rect.bottom , rect.top) 

# #win32api.SendMessage(win32gui.FindWindow(None,'阴阳师-网易游戏'),win32con.WM_,0x1b,0)

# win32api.SendMessage(win32gui.FindWindow(None,'阴阳师-网易游戏'),win32con.WM_LBUTTONDOWN,0,0x3520640)
# win32api.SendMessage(win32gui.FindWindow(None,'阴阳师-网易游戏'),win32con.WM_LBUTTONUP,0,0x3520640)

# # time.sleep(3)

# # win32api.SendMessage(win32gui.FindWindow(None,'阴阳师-网易游戏'),win32con.WM_LBUTTONDOWN,0,0)
# # win32api.SendMessage(win32gui.FindWindow(None,'阴阳师-网易游戏'),win32con.WM_LBUTTONUP,0,0)