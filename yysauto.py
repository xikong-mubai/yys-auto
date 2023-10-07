from PIL import Image
import win32gui,win32ui,win32con
import pyautogui,random
import time

# 生成随机数
def randNum(x, y):
    return round(random.uniform(x, y),3)

# 获取阴阳师运行状态
def get_windows(windowsname,filename):
    # 获取窗口句柄
    yys_handle = win32gui.FindWindow(None,windowsname)

    # 控制窗口的位置和大小 
    # 参数1：控制的窗体
    # 参数2：大致方位,HWND_TOPMOST上方
    # 参数3：位置x
    # 参数4：位置y
    # 参数5：长度
    # 参数6：宽度
    img = Image.open("img/room_wait.png")
    tmp_img_x,tmp_img_y = img.size
    win32gui.SetWindowPos(yys_handle, win32con.HWND_NOTOPMOST, 0, 0, tmp_img_x, tmp_img_y, win32con.SWP_NOACTIVATE|win32con.SWP_SHOWWINDOW)
    
    time.sleep(0.3)
    
    # 将窗口放在前台，并激活该窗口（窗口不能最小化）
    win32gui.SetForegroundWindow(yys_handle)
    time.sleep(0.3)

    # 获取窗口DC
    yys_hdDC = win32gui.GetWindowDC(yys_handle)
    
    # 根据句柄创建一个DC
    newhdDC = win32ui.CreateDCFromHandle(yys_hdDC)
    # 创建一个兼容设备内存的DC
    saveDC = newhdDC.CreateCompatibleDC()
    # 创建bitmap保存图片
    saveBitmap = win32ui.CreateBitmap()

    # 获取窗口的位置信息
    left, top, right, bottom = win32gui.GetWindowRect(yys_handle)
    if left < 0 or top < 0:
        print("请把阴阳师窗口打开至桌面（不能最小化）")
        exit(0)
    # 窗口长宽
    width = right - left
    height = bottom - top
    # bitmap初始化
    saveBitmap.CreateCompatibleBitmap(newhdDC, width, height)
    saveDC.SelectObject(saveBitmap)
    time.sleep(0.3)
    saveDC.BitBlt((0, 0), (width, height), newhdDC, (left, top), 13369376)
    time.sleep(0.3)
    saveBitmap.SaveBitmapFile(saveDC, filename)

get_windows("阴阳师-网易游戏","123.png")

num = 0
flag = eval(input("准备刷多少次？"))
print()
room_img = Image.open('./img/room_wait.png')
war1_img = Image.open('./img/war_end_1.png')
war2_img = Image.open('./img/war_end_2.png')
img_x,img_y = room_img.size

x1,y1 = room_img.size
# 0.8 , 0.25
y1 = int(0.8 * y1)
x1 = int(0.25 * x1)

x2,y2 = war1_img.size
# 0.884 , 0 - 0.10
y2 = int(0.884 * y2)
x2 = int(x2 * 0.10)

x3,y3 = war2_img.size
# 0.963 , 0.25 - 0.33
y3 = int(0.963 * y3)
x3 = int(0.33 * x3)

while True:
    get_windows("阴阳师-网易游戏","123.png")
    tmp_img = Image.open('123.png')
    
    if num >= flag:
        break

    # 判断是否在房间状态
    sum = [0,0,0]
    for i in range(0,x1,int(x1/9)):
        tmp_pixel = tmp_img.getpixel((i,y1))
        room_pixel = room_img.getpixel((i,y1))
        sum[0] += abs(tmp_pixel[0] - room_pixel[0])
        sum[1] += abs(tmp_pixel[1] - room_pixel[1])
        sum[2] += abs(tmp_pixel[2] - room_pixel[2])
    
    if abs(sum[0] / 9) < 10 and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
        # pyautogui.click(x=randNum(int(0.923 * img_x),int(0.9615 * img_x)), y=randNum(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=randNum(1,4), button='left', duration=randNum(1,3), tween=pyautogui.linear)
        tmp_pixel = tmp_img.getpixel((int(0.948 * img_x),int(0.882 * img_y)))
        
        if tmp_pixel[0] == tmp_pixel[1] and tmp_pixel[1] == tmp_pixel[2]:
            pass
        else:
            pyautogui.click(x=randNum(int(0.923 * img_x),int(0.9615 * img_x)), y=randNum(int(0.8551 * img_y),int(0.924 * img_y)))
            num += 1
            time.sleep(23)
    
    # 判断是否是结束一阶段
    sum = [0,0,0]
    for i in range(0,x2,int(x2/9)):
        tmp_pixel = tmp_img.getpixel((i,y2))
        war1_pixel = war1_img.getpixel((i,y2))
        sum[0] += abs(tmp_pixel[0] - war1_pixel[0])
        sum[1] += abs(tmp_pixel[1] - war1_pixel[1])
        sum[2] += abs(tmp_pixel[2] - war1_pixel[2])
    
    if abs(sum[0] / 9 < 10) and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
        # pyautogui.click(x=randNum(int(0.923 * img_x),int(0.9615 * img_x)), y=randNum(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=randNum(1,4), button='left', duration=randNum(1,3), tween=pyautogui.linear)
        pyautogui.click(x=randNum(int(0.923 * img_x),int(0.9615 * img_x)), y=randNum(int(0.8551 * img_y),int(0.924 * img_y)))
        time.sleep(1)
    
    # 判断是否是结束二阶段
    sum = [0,0,0]
    for i in range(x1,x3,int((x3-x1)/9)):
        tmp_pixel = tmp_img.getpixel((i,y3))
        war2_pixel = war2_img.getpixel((i,y3))
        sum[0] += abs(tmp_pixel[0] - war2_pixel[0])
        sum[1] += abs(tmp_pixel[1] - war2_pixel[1])
        sum[2] += abs(tmp_pixel[2] - war2_pixel[2])
    
    if abs(sum[0] / 9) < 10 and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
        # pyautogui.click(x=randNum(int(0.923 * img_x),int(0.9615 * img_x)), y=randNum(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=randNum(1,4), button='left', duration=randNum(1,3), tween=pyautogui.linear)
        pyautogui.click(x=randNum(int(0.923 * img_x),int(0.9615 * img_x)), y=randNum(int(0.8551 * img_y),int(0.924 * img_y)))
        time.sleep(1)
    
    print('\r\a这是第'+str(num)+'次',end='')

print("已结束！")
print("刷了"+str(num)+"次")
input("按任意键退出")

''' 获取窗口句柄名称
import win32gui

hwnd_title = dict()


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t is not "":
        print(h, t)
'''