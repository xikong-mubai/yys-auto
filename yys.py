from PIL import Image
# 获取权限
# from ctypes import windll
from sys import version_info,executable
from util import time,windll,get_windows,rand_num,mouse_click,tempimg_name,yys_window_name,init_window_pos,is_admin, \
help ,check_windows,check_user,error_exit,get_system_dpi

def click(dpi,level,x,y):
    if level > 0:
        x *= dpi
        y *= dpi
    mouse_click(yys_window_name,int(x),int(y))

# 挖土
def watu():
    get_windows(yys_window_name,tempimg_name,flag)
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
    wait_x_left = int(0.50 * img_x)
    wait_x = int(0.70 * img_x)

    # 835/887
    #war1_y = int(0.94138 * img_y)
    # 780/887
    war1_y_top = int(0.879 * img_y)
    # 17/1579
    war1_x_left = int(0.0107 * img_x)
    #war1_x = int(0.70 * img_x)

    # war2_y = int(0.963 * img_y)
    # war2_x_left = int( * img_x)
    # war2_x = int(0.33 * img_x)
    war2_x_right = int(0.9893*img_x)


    tmp_img = Image.open('./123.png')
    real_img_x,real_img_y = tmp_img.size
    tmp_img.close()
    real_wait_y = int(0.8 * real_img_y)
    real_wait_x_left = int(0.50 * real_img_x)
    real_wait_x = int(0.70 * real_img_x)

    # 835/887
    #war1_y = int(0.94138 * img_y)
    # 780/887
    real_war1_y_top = int(0.879 * real_img_y)
    # 17/1579
    real_war1_x_left = int(0.0107 * real_img_x)
    #war1_x = int(0.70 * img_x)

    # war2_y = int(0.963 * img_y)
    # war2_x_left = int( * img_x)
    # war2_x = int(0.33 * img_x)
    real_war2_x_right = int(0.9893*real_img_x)


    while num < watu_num:
        while True:
            get_windows(yys_window_name,tempimg_name,flag)
            tmp_img = Image.open('123.png')

            # 判断是否在房间状态
            pixel_sum = [0,0,0]
            img_pixel = []
            for i in range(wait_x_left,wait_x,int((wait_x-wait_x_left)/9)):
                img_pixel.append(room_img.getpixel((i,wait_y)))
            tmp_pixel = []
            for i in range(real_wait_x_left,real_wait_x,int((real_wait_x - real_wait_x_left)/9)):
                tmp_pixel.append(tmp_img.getpixel((i,real_wait_y)))        
            length = min(len(tmp_pixel),len(img_pixel))
            for i in range(length):
                pixel_sum[0] += abs(tmp_pixel[i][0] - img_pixel[i][0])
                pixel_sum[1] += abs(tmp_pixel[i][1] - img_pixel[i][1])
                pixel_sum[2] += abs(tmp_pixel[i][2] - img_pixel[i][2])
            if abs(pixel_sum[0] / length) < 10 and abs(pixel_sum[1] / length) < 10 and abs(pixel_sum[2] / length) < 10:
                result_flag = 0
                # 1503/1579  790/887
                tmp_pixel = tmp_img.getpixel((int(0.95 * real_img_x),int(0.8901 * real_img_y)))
                # 1464/1579  807-826 /887
                wait_button_pixel_1 = tmp_img.getpixel((int(0.92717 * real_img_x),int(0.92108 * real_img_y)))
                wait_button_pixel_2 = room_member_img.getpixel((int(0.92717 * img_x),int(0.92108 * img_y)))
                wait_button_pixel = [
                    wait_button_pixel_1[0] - wait_button_pixel_2[0],
                    wait_button_pixel_1[1] - wait_button_pixel_2[1],
                    wait_button_pixel_1[2] - wait_button_pixel_2[2]
                ]
                if tmp_pixel[0] == tmp_pixel[1] and tmp_pixel[1] == tmp_pixel[2]:
                    print("\r等待成员中",end='')
                elif abs(wait_button_pixel[0]) < 5 and abs(wait_button_pixel[1]) < 5 and abs(wait_button_pixel[2]) < 5:
                    print("\r等待房主中",end='')
                else:
                    # 1480-1540 / 1579   762-820 / 887
                    x=rand_num(int(0.9373 * init_x),int(0.9653 * init_x))
                    y=rand_num(int(0.8791 * init_y),int(0.91446 * init_y))
                    mouse_click(yys_window_name,int(x),int(y))
                    print("\r开始")
                    time.sleep(10)
            
            # 判断是否是结束一阶段
            pixel_sum = [0,0,0]
            img_pixel = []
            for i in range(war1_y_top,img_y,int((img_y-war1_y_top)/9)):
                img_pixel.append(war1_img.getpixel((war1_x_left,i)))
            tmp_pixel = []
            for i in range(real_war1_y_top,real_img_y,int((real_img_y - real_war1_y_top)/9)):
                tmp_pixel.append(tmp_img.getpixel((real_war1_x_left,i)))        
            length = min(len(tmp_pixel),len(img_pixel))
            for i in range(length):    
                pixel_sum[0] += abs(tmp_pixel[i][0] - img_pixel[i][0])
                pixel_sum[1] += abs(tmp_pixel[i][1] - img_pixel[i][1])
                pixel_sum[2] += abs(tmp_pixel[i][2] - img_pixel[i][2])
            
            if abs(pixel_sum[0] / length) < 5 and abs(pixel_sum[1] / length) < 5 and abs(pixel_sum[2] / length) < 5:
                x=rand_num(int(0.87 * init_x),int(0.93 * init_x))
                y=rand_num(int(0.85 * init_y),int(0.93 * init_y))
                mouse_click(yys_window_name,int(x),int(y))
                print("\r结算画面一阶段")
                time.sleep(0.3)
            
            # 判断是否是结束二阶段
            pixel_sum = [0,0,0]
            img_pixel = []
            for i in range(war1_y_top,img_y,int((img_y-war1_y_top)/9)):
                img_pixel.append(war2_img.getpixel((war2_x_right,i)))
            tmp_pixel = []
            for i in range(real_war1_y_top,real_img_y,int((real_img_y - real_war1_y_top)/9)):
                tmp_pixel.append(tmp_img.getpixel((real_war2_x_right,i)))        
            length = min(len(tmp_pixel),len(img_pixel))
            for i in range(length):    
                pixel_sum[0] += abs(tmp_pixel[i][0] - img_pixel[i][0])
                pixel_sum[1] += abs(tmp_pixel[i][1] - img_pixel[i][1])
                pixel_sum[2] += abs(tmp_pixel[i][2] - img_pixel[i][2])
            if abs(pixel_sum[0] / length) < 5 and abs(pixel_sum[1] / length) < 5 and abs(pixel_sum[2] / length) < 5:
                # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
                x=rand_num(int(0.87 * init_x),int(0.93 * init_x))
                y=rand_num(int(0.85 * init_y),int(0.93 * init_y))
                mouse_click(yys_window_name,int(x),int(y))
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

# def yuling():
#     get_windows(yys_window_name,tempimg_name,flag)

#     while True:
#         day = input("打哪个御灵，从左往右按御灵的开放日期算（比如周二暗神龙就输入一个“2”）：")
#         yuling_img = ''
#         if len(day) != 1:
#             print("请按照例子输入，否则我不认识的嗷")
#         else:
#             if day == "2":
#                 yuling_img = 'yuling_2'
#             elif day == '3':
#                 yuling_img = 'yuling_3'
#             elif day == '4':
#                 yuling_img = 'yuling_4'
#             elif day == '5':
#                 yuling_img = 'yuling_5'
#             else:
#                 print('我不认识它呢亲亲')
#                 continue
#             break
#     num = 0
#     flag = eval(input("准备刷多少次？"))
#     print()
#     room_img = Image.open('./img/'+yuling_img+'/yuling_start.png')
#     war1_img = Image.open('./img/'+yuling_img+'/yuling_end_1.png')
#     war2_img = Image.open('./img/'+yuling_img+'/yuling_end_2.png')
#     defeat_img = Image.open('./img/defeat.png')
#     img_x,img_y = room_img.size

#     x1,y1 = room_img.size
#     # 1153  679  370   425
#     y1 = int(425/679 * y1)
#     x1_2 = int(300/1153 * x1)
#     x1_1 = int(75/1153 * x1)

#     x2,y2 = war1_img.size
#     # 0.884 , 0 - 0.10
#     y2 = int(0.884 * y2)
#     x2_2 = int(x2 * 0.10)
#     x2_1 = int(15/1153 * x2)

#     x3,y3 = war2_img.size
#     # 0.963 , 0.25 - 0.33
#     y3 = int(0.963 * y3)
#     x3 = int(0.33 * x3)

#     x4,y4 = defeat_img.size
#     # 1152,681  300,180 -> 480,180
#     x4_1 = int(300/1152 * x4)
#     x4_2 = int(480/1152 * x4)
#     y4 = int(180/681 * y4)

#     while True:
#         get_windows(yys_window_name,tempimg_name,flag)
#         tmp_img = Image.open('123.png')
        
#         if num >= flag:
#             break

#         # 判断是否在房间状态
#         pixel_sum = [0,0,0]
#         for i in range(x1_1,x1_2,int((x1_2-x1_1)/9)):
#             tmp_pixel = tmp_img.getpixel((i,y1))
#             room_pixel = room_img.getpixel((i,y1))
#             pixel_sum[0] += abs(tmp_pixel[0] - room_pixel[0])
#             pixel_sum[1] += abs(tmp_pixel[1] - room_pixel[1])
#             pixel_sum[2] += abs(tmp_pixel[2] - room_pixel[2])
        
#         if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
#             # pyautogui.click(x=rand_num(int(0.8987 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
#             pyautogui.click(x=rand_num(int(0.872 * img_x),int(0.925 * img_x)), y=rand_num(int(0.85 * img_y),int(0.932 * img_y)))
#             num += 1
#             time.sleep(10)
        
#         # 判断是否是结束一阶段
#         pixel_sum = [0,0,0]
#         for i in range(x2_1,x2_2,int((x2_2-x2_1)/9)):
#             tmp_pixel = tmp_img.getpixel((i,y2))
#             war1_pixel = war1_img.getpixel((i,y2))
#             pixel_sum[0] += abs(tmp_pixel[0] - war1_pixel[0])
#             pixel_sum[1] += abs(tmp_pixel[1] - war1_pixel[1])
#             pixel_sum[2] += abs(tmp_pixel[2] - war1_pixel[2])
        
#         if abs(pixel_sum[0] / 9 < 10) and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
#             # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
#             pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
#             time.sleep(0.3)
        
#         # 判断是否是结束二阶段
#         pixel_sum = [0,0,0]
#         for i in range(x2_2,x3,int((x3-x2_2)/9)):
#             tmp_pixel = tmp_img.getpixel((i,y3))
#             war2_pixel = war2_img.getpixel((i,y3))
#             pixel_sum[0] += abs(tmp_pixel[0] - war2_pixel[0])
#             pixel_sum[1] += abs(tmp_pixel[1] - war2_pixel[1])
#             pixel_sum[2] += abs(tmp_pixel[2] - war2_pixel[2])
        
#         if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
#             # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
#             pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
#             time.sleep(0.3)
        
#         # 判断是否是 defeat
#         pixel_sum = [0,0,0]
#         for i in range(x4_1,x4_2,int((x4_2-x4_1)/9)):
#             tmp_pixel = tmp_img.getpixel((i,y4))
#             defeat_pixel = defeat_img.getpixel((i,y4))
#             pixel_sum[0] += abs(tmp_pixel[0] - defeat_pixel[0])
#             pixel_sum[1] += abs(tmp_pixel[1] - defeat_pixel[1])
#             pixel_sum[2] += abs(tmp_pixel[2] - defeat_pixel[2])
        
#         if abs(pixel_sum[0] / 9) < 10 and abs(pixel_sum[1] / 9) < 10 and abs(pixel_sum[2] / 10) < 10:
#             # pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
#             pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
#             time.sleep(0.3)

#         print('\r这是第'+str(num)+'次',end='')
    
#     print("已结束！")
#     print("刷了"+str(num)+"次")
#     print()


#ctypes.windll.shcore.SetProcessDpiAwareness(2)
#yys_path = input("请输入阴阳师程序路径：")
#os.system(yys_path)
print("请稍等，正在加载资源......")

x,y = 1050,572
#windll.shcore.SetProcessDpiAwareness(0)
if is_admin():
    #windll.shcore.SetProcessDpiAwareness(0)
    global flag,dpi,a
    flag = 0
    # 为空会获取到资源管理器的子窗口pid（空窗口）
    yys_window_name = input("请输入目标窗口名称：")
    if not check_windows(yys_window_name):
        error_exit()

    print("当前目标窗口dpi及其dpi感知级别：",end='')
    dpi,a = get_system_dpi(yys_window_name)
    print(dpi,a)
    print("当前窗口dpi及其dpi感知级别：",end='')
    dpi,a = get_system_dpi('')
    print(dpi,a)

    # img_x,img_y = 1180,702
    # img_x,img_y = img_x + int(22/dpi),img_y + int((45+2+10)/dpi)# 769 462 # dpi为 1.5 时，等比放大后即为 1131 636
    global global_x,global_y,init_x,init_y
    init_x,init_y = 754,424 # 预设画面宽高
    if a == -1 or a == 0:
        flag |= 2
        chang_x,chang_y = 22/dpi,57/dpi
        global_x = init_x + int(chang_x)
        global_x = global_x + 1 if chang_x - int(chang_x) > 0 else global_x
        global_y = init_y + int(chang_y)
        global_y = global_y + 1 if chang_y - int(chang_y) > 0 else global_y  
    else:
        global_x = init_x + 22
        global_y = init_y + 57

    print("预设窗口宽高为：",global_x,global_y)
    print("初始化窗口位置...")
    init_window_pos(yys_window_name,global_x,global_y)
    print("初始化窗口完成")

    config_file = open('./config','a+',encoding='utf-8')
    config_file.seek(0)
    yys_name = config_file.read()
    if len(yys_name) != 0:
        choose = input("请确认 "+yys_name+" 是否为你的阴阳师昵称（y/n）：")
        if choose.lower() == 'y':
            pass
        elif choose.lower() == 'n':
            yys_name = input("请手动输入阴阳师用户名称：")
        else:
            print('请输入 y 或者 n。')
            config_file.close()
            error_exit()
    else:
        yys_name = input("请手动输入阴阳师用户名称：")
    config_file.truncate(0)
    config_file.write(yys_name)
    config_file.close()
    if not check_user(yys_name):
        error_exit()
    
    while True:
        help()
        choose = input('请选择模式：')
        if choose == '1':
            watu()
        #elif flag == '2':
        #    yuling()
        elif choose == '0':
            error_exit()
        elif choose == '5':
            flag |= 1
        else:
            print('对叭起, 我不认识它QAQ')
else:
    if version_info[0] == 3:
        windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
    # else:  # in python2.x
    #     windll.shell32.ShellExecuteW(None, u"runas", unicode(executable), unicode(__file__), None, 1)
    #     pass
