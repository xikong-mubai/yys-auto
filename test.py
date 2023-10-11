import win32gui,win32ui,win32con,win32com.client,random,win32api,win32print
from PIL import Image
from ctypes import windll
import pyautogui,time,pythoncom
# 获取权限
import ctypes, sys, os

try:
    f = ctypes.windll.dwmapi.DwmGetWindowAttribute
except WindowsError:
    f = None
if f: # Vista & 7 stuff
    rect = ctypes.wintypes.RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    f(ctypes.wintypes.HWND(win32gui.FindWindow(None,'阴阳师-网易游戏')),
      ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
      ctypes.byref(rect),
      ctypes.sizeof(rect)
      )
    size = (rect.right - rect.left, rect.bottom - rect.top)        
else:      
    size = (1)
print(win32gui.FindWindow(None,'阴阳师-网易游戏'))
print(size)