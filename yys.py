import win32gui,win32ui,win32con,win32com.client,random
from PIL import Image
import pyautogui,time,pythoncom
# 获取权限
import ctypes, sys, os
from .util import is_admin,get_windows,rand_num

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

# 挖土
def watu():
    get_windows(yys_window_name,tempimg_name)
    #get_windows('readme.txt - 记事本','123.png')
    num = 0
    flag = eval(input("准备刷多少次？"))
    print()
    room_img = Image.open('./img/room_wait.png')
    war1_img = Image.open('./img/war_end_1.png')
    war2_img = Image.open('./img/war_end_2.png')
    defeat_img = Image.open('./img/defeat.png')
    img_x,img_y = room_img.size

    x1,y1 = room_img.size
    # 0.8 , 0.25
    y1 = int(0.8 * y1)
    x1_1 = int(20/1153 * x1)
    x1 = int(0.25 * x1)

    x2,y2 = war1_img.size
    # 0.884 , 0 - 0.10
    y2 = int(0.884 * y2)
    x2 = int(x2 * 0.10)

    x3,y3 = war2_img.size
    # 0.963 , 0.25 - 0.33
    y3 = int(0.963 * y3)
    x3 = int(0.33 * x3)

    x4,y4 = defeat_img.size
    # 1152,681  300,180 -> 480,180
    x4_1 = int(300/1152 * x4)
    x4_2 = int(480/1152 * x4)
    y4 = int(180/681 * y4)

    while True:
        get_windows(yys_window_name,tempimg_name)
        tmp_img = Image.open('123.png')
        
        if num >= flag:
            break

        # 判断是否在房间状态
        pixel_sum = [0,0,0]
        for i in range(x1_1,x1,int((x1-x1_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y1))
            room_pixel = room_img.getpixel((i,y1))
            pixel_sum[0] += abs(tmp_pixel[0] - room_pixel[0])
            pixel_sum[1] += abs(tmp_pixel[1] - room_pixel[1])
            pixel_sum[2] += abs(tmp_pixel[2] - room_pixel[2])
        
        if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            tmp_pixel = tmp_img.getpixel((int(0.948 * img_x),int(0.882 * img_y)))
            
            if tmp_pixel[0] == tmp_pixel[1] and tmp_pixel[1] == tmp_pixel[2]:
                pass
            else:
                pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
                num += 1
                time.sleep(23)
        
        # 判断是否是结束一阶段
        pixel_sum = [0,0,0]
        for i in range(x1_1,x2,int((x2-x1_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y2))
            war1_pixel = war1_img.getpixel((i,y2))
            pixel_sum[0] += abs(tmp_pixel[0] - war1_pixel[0])
            pixel_sum[1] += abs(tmp_pixel[1] - war1_pixel[1])
            pixel_sum[2] += abs(tmp_pixel[2] - war1_pixel[2])
        
        if abs(pixel_sum[0] / 9 < 10) and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            time.sleep(0.3)
        
        # 判断是否是结束二阶段
        pixel_sum = [0,0,0]
        for i in range(x1,x3,int((x3-x1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y3))
            war2_pixel = war2_img.getpixel((i,y3))
            pixel_sum[0] += abs(tmp_pixel[0] - war2_pixel[0])
            pixel_sum[1] += abs(tmp_pixel[1] - war2_pixel[1])
            pixel_sum[2] += abs(tmp_pixel[2] - war2_pixel[2])
        
        if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            time.sleep(0.3)

        # 判断是否是 defeat
        pixel_sum = [0,0,0]
        for i in range(x4_1,x4_2,int((x4_2-x4_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y4))
            defeat_pixel = defeat_img.getpixel((i,y4))
            pixel_sum[0] += abs(tmp_pixel[0] - defeat_pixel[0])
            pixel_sum[1] += abs(tmp_pixel[1] - defeat_pixel[1])
            pixel_sum[2] += abs(tmp_pixel[2] - defeat_pixel[2])
        
        if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            time.sleep(0.3)
        
        print('\r这是第'+str(num)+'次',end='')

    print("已结束！")
    print("刷了"+str(num)+"次")
    print()

def yuling():
    get_windows(yys_window_name,tempimg_name)

    while True:
        day = input("打哪个御灵，从左往右按御灵的开放日期算（比如周二暗神龙就输入一个“2”）：")
        yuling_img = ''
        if len(day) != 1:
            print("请按照例子输入，否则我不认识的嗷")
        else:
            if day == "2":
                yuling_img = 'yuling_2'
            elif day == '3':
                yuling_img = 'yuling_3'
            elif day == '4':
                yuling_img = 'yuling_4'
            elif day == '5':
                yuling_img = 'yuling_5'
            else:
                print('我不认识它呢亲亲')
                continue
            break
    num = 0
    flag = eval(input("准备刷多少次？"))
    print()
    room_img = Image.open('./img/'+yuling_img+'/yuling_start.png')
    war1_img = Image.open('./img/'+yuling_img+'/yuling_end_1.png')
    war2_img = Image.open('./img/'+yuling_img+'/yuling_end_2.png')
    defeat_img = Image.open('./img/defeat.png')
    img_x,img_y = room_img.size

    x1,y1 = room_img.size
    # 1153  679  370   425
    y1 = int(425/679 * y1)
    x1_2 = int(300/1153 * x1)
    x1_1 = int(75/1153 * x1)

    x2,y2 = war1_img.size
    # 0.884 , 0 - 0.10
    y2 = int(0.884 * y2)
    x2_2 = int(x2 * 0.10)
    x2_1 = int(15/1153 * x2)

    x3,y3 = war2_img.size
    # 0.963 , 0.25 - 0.33
    y3 = int(0.963 * y3)
    x3 = int(0.33 * x3)

    x4,y4 = defeat_img.size
    # 1152,681  300,180 -> 480,180
    x4_1 = int(300/1152 * x4)
    x4_2 = int(480/1152 * x4)
    y4 = int(180/681 * y4)

    while True:
        get_windows(yys_window_name,tempimg_name)
        tmp_img = Image.open('123.png')
        
        if num >= flag:
            break

        # 判断是否在房间状态
        sum = [0,0,0]
        for i in range(x1_1,x1_2,int((x1_2-x1_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y1))
            room_pixel = room_img.getpixel((i,y1))
            sum[0] += abs(tmp_pixel[0] - room_pixel[0])
            sum[1] += abs(tmp_pixel[1] - room_pixel[1])
            sum[2] += abs(tmp_pixel[2] - room_pixel[2])
        
        if abs(sum[0] / 9) < 10 and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.8987 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.872 * img_x),int(0.925 * img_x)), y=rand_num(int(0.85 * img_y),int(0.932 * img_y)))
            num += 1
            time.sleep(10)
        
        # 判断是否是结束一阶段
        sum = [0,0,0]
        for i in range(x2_1,x2_2,int((x2_2-x2_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y2))
            war1_pixel = war1_img.getpixel((i,y2))
            sum[0] += abs(tmp_pixel[0] - war1_pixel[0])
            sum[1] += abs(tmp_pixel[1] - war1_pixel[1])
            sum[2] += abs(tmp_pixel[2] - war1_pixel[2])
        
        if abs(sum[0] / 9 < 10) and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            time.sleep(0.3)
        
        # 判断是否是结束二阶段
        sum = [0,0,0]
        for i in range(x2_2,x3,int((x3-x2_2)/9)):
            tmp_pixel = tmp_img.getpixel((i,y3))
            war2_pixel = war2_img.getpixel((i,y3))
            sum[0] += abs(tmp_pixel[0] - war2_pixel[0])
            sum[1] += abs(tmp_pixel[1] - war2_pixel[1])
            sum[2] += abs(tmp_pixel[2] - war2_pixel[2])
        
        if abs(sum[0] / 9) < 10 and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            time.sleep(0.3)
        
        # 判断是否是 defeat
        sum = [0,0,0]
        for i in range(x4_1,x4_2,int((x4_2-x4_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y4))
            defeat_pixel = defeat_img.getpixel((i,y4))
            sum[0] += abs(tmp_pixel[0] - defeat_pixel[0])
            sum[1] += abs(tmp_pixel[1] - defeat_pixel[1])
            sum[2] += abs(tmp_pixel[2] - defeat_pixel[2])
        
        if abs(sum[0] / 9) < 10 and abs(sum[1] / 9) < 10 and abs(sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            time.sleep(0.3)

        print('\r这是第'+str(num)+'次',end='')
    
    print("已结束！")
    print("刷了"+str(num)+"次")
    print()

print("请稍等，正在加载资源......")

if is_admin():
    while True:
        help()
        flag = input('请选择模式：')
        if flag == '1':
            watu()
        elif flag == '2':
            yuling()
        elif flag == '0':
            exit(0)
        else:
            print('对叭起, 我不认识它QAQ')
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:  # in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
        pass
