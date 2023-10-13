from PIL import Image
import pyautogui
# 获取权限
# from ctypes import windll
from sys import version_info,executable
from util import time,windll,get_windows,rand_num,mouse_click,tempimg_name,yys_window_name,init_window_pos,is_admin, \
help ,check_windows,check_user,error_exit

# 挖土
def watu():
    get_windows(yys_window_name,tempimg_name)
    #get_windows('readme.txt - 记事本','123.png')
    num = 0 ; result_flag = 0
    watu_num = eval(input("准备刷多少次？"))
    print()
    room_img = Image.open('./img/room_wait.png')
    room_member_img = Image.open('./img/room_wait_member_1.png')
    # check_window(room_img)
    war1_img = Image.open('./img/war_end_1.png')
    # check_window(war1_img)
    war2_img = Image.open('./img/war_end_2.png')
    # check_window(war2_img)
    defeat_img = Image.open('./img/defeat.png')
    # check_window(defeat_img)

    img_x,img_y = room_img.size

    wait_y = int(0.8 * img_y)
    wait_x_left = int(0.1 * img_x)
    wait_x = int(0.30 * img_x)

    war1_y = int(0.9375 * img_y)
    war1_x = int(0.0625 * img_x)

    war2_y = int(0.963 * img_y)
    war2_x = int(0.33 * img_x)

    while num < watu_num:
        while True:
            get_windows(yys_window_name,tempimg_name)
            tmp_img = Image.open('123.png')

            # 判断是否在房间状态
            pixel_sum = [0,0,0]
            for i in range(wait_x_left,wait_x,int((wait_x-wait_x_left)/9)):
                tmp_pixel = tmp_img.getpixel((i,wait_y))
                room_pixel = room_img.getpixel((i,wait_y))
                pixel_sum[0] += abs(tmp_pixel[0] - room_pixel[0])
                pixel_sum[1] += abs(tmp_pixel[1] - room_pixel[1])
                pixel_sum[2] += abs(tmp_pixel[2] - room_pixel[2])
            
            if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
                # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
                result_flag = 0
                tmp_pixel = tmp_img.getpixel((int(0.95 * img_x),int(0.9 * img_y)))
                center_pixel = tmp_img.getpixel((int(0.50317 * img_x),int(0.6044 * img_y)))
                wait_button_pixel_1 = tmp_img.getpixel((int(0.92649 * img_x),int(0.9276 * img_y)))
                wait_button_pixel_2 = room_member_img.getpixel((int(0.92649 * img_x),int(0.9276 * img_y)))
                wait_button_pixel = [
                    wait_button_pixel_1[0] - wait_button_pixel_2[0],
                    wait_button_pixel_1[1] - wait_button_pixel_2[1],
                    wait_button_pixel_1[2] - wait_button_pixel_2[2]
                ]
                if tmp_pixel[0] == tmp_pixel[1] and tmp_pixel[1] == tmp_pixel[2]:
                    print("\r等待成员中",end='')
                #elif center_pixel[0] > 250 and center_pixel[1] > 250 and center_pixel[2] > 250:
                #    print("\r等待房主中",end='')
                elif abs(wait_button_pixel[0]) < 5 and abs(wait_button_pixel[1]) < 5 and abs(wait_button_pixel[2]) < 5:
                    print("\r等待房主中",end='')
                else:
                    x=rand_num(int(0.925 * img_x),int(0.975 * img_x))
                    y=rand_num(int(0.87 * img_y),int(0.93 * img_y))
                    mouse_click(yys_window_name,x,y)
                    print("\r等待成员中")
                    print("\r开始")
                    time.sleep(10)
            
            # 判断是否是结束一阶段
            pixel_sum = [0,0,0]
            for i in range(5,war1_x,int((war1_x-5)/9)):
                tmp_pixel = tmp_img.getpixel((i,war1_y))
                war1_pixel = war1_img.getpixel((i,war1_y))
                pixel_sum[0] += abs(tmp_pixel[0] - war1_pixel[0])
                pixel_sum[1] += abs(tmp_pixel[1] - war1_pixel[1])
                pixel_sum[2] += abs(tmp_pixel[2] - war1_pixel[2])
            
            if abs(pixel_sum[0] / 9 < 10) and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
                x=rand_num(int(0.9 * img_x),int(0.98 * img_x))
                y=rand_num(int(0.85 * img_y),int(0.95 * img_y))
                mouse_click(yys_window_name,x,y)
                print("\r结算画面一阶段")
                time.sleep(0.3)
            
            # 判断是否是结束二阶段
            pixel_sum = [0,0,0]
            for i in range(war1_x,war2_x,int((war2_x-war1_x)/9)):
                tmp_pixel = tmp_img.getpixel((i,war2_y))
                war2_pixel = war2_img.getpixel((i,war2_y))
                pixel_sum[0] += abs(tmp_pixel[0] - war2_pixel[0])
                pixel_sum[1] += abs(tmp_pixel[1] - war2_pixel[1])
                pixel_sum[2] += abs(tmp_pixel[2] - war2_pixel[2])

            if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
                # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
                x=rand_num(int(0.9 * img_x),int(0.98 * img_x))
                y=rand_num(int(0.85 * img_y),int(0.95 * img_y))
                mouse_click(yys_window_name,x,y)
                print("\r结算画面二阶段")
                if result_flag == 0:
                    result_flag = 1
                    num += 1
                time.sleep(0.3)
                break

            # # 判断是否是 defeat
            # pixel_sum = [0,0,0]
            # for i in range(x4_1,x4_2,int((x4_2-x4_1)/9)):
            #     tmp_pixel = tmp_img.getpixel((i,y4))
            #     defeat_pixel = defeat_img.getpixel((i,y4))
            #     pixel_sum[0] += abs(tmp_pixel[0] - defeat_pixel[0])
            #     pixel_sum[1] += abs(tmp_pixel[1] - defeat_pixel[1])
            #     pixel_sum[2] += abs(tmp_pixel[2] - defeat_pixel[2])
            
            # if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
            #     # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            #     pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
            #     time.sleep(0.3)
            
            tmp_img.close()
        
        print('\r这是第'+str(num)+'次')

    room_img.close()
    room_member_img.close()
    war1_img.close()
    war2_img.close()
    defeat_img.close()
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
        pixel_sum = [0,0,0]
        for i in range(x1_1,x1_2,int((x1_2-x1_1)/9)):
            tmp_pixel = tmp_img.getpixel((i,y1))
            room_pixel = room_img.getpixel((i,y1))
            pixel_sum[0] += abs(tmp_pixel[0] - room_pixel[0])
            pixel_sum[1] += abs(tmp_pixel[1] - room_pixel[1])
            pixel_sum[2] += abs(tmp_pixel[2] - room_pixel[2])
        
        if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
            # pyautogui.click(x=rand_num(int(0.8987 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
            pyautogui.click(x=rand_num(int(0.872 * img_x),int(0.925 * img_x)), y=rand_num(int(0.85 * img_y),int(0.932 * img_y)))
            num += 1
            time.sleep(10)
        
        # 判断是否是结束一阶段
        pixel_sum = [0,0,0]
        for i in range(x2_1,x2_2,int((x2_2-x2_1)/9)):
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
        for i in range(x2_2,x3,int((x3-x2_2)/9)):
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

print("请稍等，正在加载资源......")

if is_admin():
    #ctypes.windll.shcore.SetProcessDpiAwareness(2)
    #yys_path = input("请输入阴阳师程序路径：")
    #os.system(yys_path)
    config_file = open('./config','a+',encoding='utf-8')
    config_file.seek(0)
    yys_name = config_file.read()
    if len(yys_name) != 0:
        flag = input("请确认 "+yys_name+" 是否为你的阴阳师昵称（y/n）：")
        if flag.lower() == 'y':
            pass
        elif flag.lower() == 'n':
            yys_name = input("请输入阴阳师用户名称：")
        else:
            print('请输入 y 或者 n。')
            config_file.close()
            error_exit()
    else:
        yys_name = input("请输入阴阳师用户名称：")
    config_file.truncate(0)
    config_file.write(yys_name)
    config_file.close()
    if not check_user(yys_name):
        error_exit()
    
    # 为空会获取到资源管理器的子窗口pid（空窗口）
    yys_window_name = input("请输入目标窗口名称：")
    if not check_windows(yys_window_name):
        error_exit()
    print("获取初始图像尺寸：",end='')
    try:
        room_img = Image.open('./img/room_wait.png')
        img_x,img_y = room_img.size
        print(img_x,img_y)
        room_img.close()
    except Exception as e:
        print("获取图像失败",e)
        error_exit()
    print("初始化窗口位置...")
    init_window_pos(yys_window_name,img_x,img_y)
    print("初始化窗口完成")
    while True:
        help()
        flag = input('请选择模式：')
        if flag == '1':
            watu()
        #elif flag == '2':
        #    yuling()
        elif flag == '0':
            exit(0)
        else:
            print('对叭起, 我不认识它QAQ')
else:
    if version_info[0] == 3:
        windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
    # else:  # in python2.x
    #     windll.shell32.ShellExecuteW(None, u"runas", unicode(executable), unicode(__file__), None, 1)
    #     pass
