# 获取权限
# from ctypes import windll
import config
from sys import version_info,executable
from util import sleep,windll,get_windows,rand_num,mouse_click,yys_window_name,init_window_pos,is_admin, \
help ,check_windows,check_user,error_exit,get_system_dpi,Image,update,json,action

# def yuling():
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
#     num = 0 ; result_flag = 0
#     yuling_num = eval(input("准备刷多少次？"))
#     start_img = Image.open('./img/'+yuling_img+'/yuling_start.png')
#     war1_img = Image.open('./img/'+yuling_img+'/yuling_end_1.png')
#     war2_img = Image.open('./img/'+yuling_img+'/yuling_end_2.png')
#     # defeat_img = Image.open('./img/defeat.png')
#     img_x,img_y = start_img.size
#     tmp = get_windows(yys_window_hwnd,mode_flag)
#     real_x,real_y = tmp.size
#     tmp.close()
#     x1,y1 = start_img.size
#     # 1153  679  370   425
#     y1 = int(425/679 * y1)
#     x1_2 = int(300/1153 * x1)
#     x1_1 = int(75/1153 * x1)
#     real_y1 = int(425/679 * real_y)
#     real_x1_2 = int(300/1153 * real_x)
#     real_x1_1 = int(75/1153 * real_x)

#     x2,y2 = war1_img.size
#     # 0.884 , 0 - 0.10
#     y2 = int(0.884 * y2)
#     x2_2 = int(x2 * 0.10)
#     x2_1 = int(15/1153 * x2)
#     real_y2 = int(425/679 * real_y)
#     real_x2_2 = int(300/1153 * real_x)
#     real_x2_1 = int(75/1153 * real_x)

#     x3,y3 = war2_img.size
#     # 0.963 , 0.25 - 0.33
#     y3 = int(0.963 * y3)
#     x3 = int(0.33 * x3)
#     real_y3 = int(425/679 * real_y)
#     real_x3_2 = int(300/1153 * real_x)
#     real_x4_1 = int(75/1153 * real_x)

#     # x4,y4 = defeat_img.size
#     # # 1152,681  300,180 -> 480,180
#     # x4_1 = int(300/1152 * x4)
#     # x4_2 = int(480/1152 * x4)
#     # y4 = int(180/681 * y4)

#     while True:
#         tmp_img = get_windows(yys_window_hwnd,mode_flag)
        
#         if num >= yuling_num:
#             break

#         # 判断是否在房间状态
#         pixel_sum = [0,0,0]
#         img_pixel = []
#         for i in range(x1_1,x1_2,int((x1_2-x1_1)/9)):
#             img_pixel.append(start_img.getpixel((i,y1)))
#         tmp_pixel = []
#         for i in range(real_x1_1,real_x1_2,int((real_x1_2 - real_x1_1)/9)):
#             tmp_pixel.append(tmp_img.getpixel((i,real_y1)))        
#         length = min(len(tmp_pixel),len(img_pixel))
#         for i in range(length):
#             pixel_sum[0] += abs(tmp_pixel[i][0] - img_pixel[i][0])
#             pixel_sum[1] += abs(tmp_pixel[i][1] - img_pixel[i][1])
#             pixel_sum[2] += abs(tmp_pixel[i][2] - img_pixel[i][2])
        
#         if abs(pixel_sum[0] / length) < 5 and abs(pixel_sum[1] / length) < 5 and abs(pixel_sum[2] / length) < 5:
#             # pyautogui.click(x=rand_num(int(0.8987 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)), clicks=1, interval=rand_num(1,4), button='left', duration=rand_num(1,3), tween=pyautogui.linear)
#             #pyautogui.click(x=rand_num(int(0.872 * img_x),int(0.925 * img_x)), y=rand_num(int(0.85 * img_y),int(0.932 * img_y)))
#             x=rand_num(int(0.872 * img_x),int(0.925 * img_x))
#             y=rand_num(int(0.85 * img_y),int(0.932 * img_y))
#             mouse_click(yys_window_hwnd,int(x),int(y))
#             result_flag = 0
#             sleep(0.5)
        
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
#             #pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
#             x=rand_num(int(0.923 * img_x),int(0.9615 * img_x))
#             y=rand_num(int(0.8551 * img_y),int(0.924 * img_y))
#             mouse_click(yys_window_hwnd,int(x),int(y))
#             sleep(0.3)
        
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
#             #pyautogui.click(x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)), y=rand_num(int(0.8551 * img_y),int(0.924 * img_y)))
#             x=rand_num(int(0.923 * img_x),int(0.9615 * img_x)),
#             y=rand_num(int(0.8551 * img_y),int(0.924 * img_y))
#             mouse_click(yys_window_hwnd,int(x),int(y))
#             if result_flag == 0:
#                 result_flag = 1
#                 num += 1
#             sleep(0.3)
        
        # 判断是否是 defeat
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
        #     sleep(0.3)

    #     print('\r这是第'+str(num)+'次            ',end='')
    
    # print("已结束！")
    # print("刷了"+str(num)+"次")
    # print()

def save_img():
    num = 0
    while True:
        choose = input("请将游戏运行至想要截取的画面，然后输入 1 进行画面截取。输入 0 返回主菜单")
        if choose == '0':
            return
        elif choose == '1':
            window = get_windows(config.yys_window_hwnd,mode_flag)
            window.save('./img/tmp_'+str(num)+".png")
            num += 1
            window.close()
        
# ctypes.windll.shcore.SetProcessDpiAwareness(2)
# yys_path = input("请输入阴阳师程序路径：")
# os.system(yys_path)

if __name__ == "__main__":
    update()
    print("请稍等，正在加载资源......")

    x,y = 1050,572
    # windll.shcore.SetProcessDpiAwareness(0)
    if is_admin():
        # windll.shcore.SetProcessDpiAwareness(0)
        mode_flag = 0
        # 为空会获取到资源管理器的子窗口pid（空窗口）
        yys_window_name = input("请输入目标窗口名称：")
        result,windows = check_windows(yys_window_name)
        while not result:
            print("未检测到目标窗口名称。")
            yys_window_name = input("请重新输入目标窗口名称：")
            result,windows = check_windows(yys_window_name)
        choose = 0
        if len(windows) > 1:
            print('检测到多个目标窗口，基础信息如下：')
            for i in range(len(windows)):
                print(i,'、',windows[i])
            while True:
                choose = input("请选择目标窗口序号：").strip()
                try:
                    choose = int(choose)
                    if choose < 0 or choose >= len(windows):
                        raise Exception("序号输入错误")
                    break
                except Exception as e:
                    print(e)
        config.yys_window_hwnd = windows[choose][0]

        print("当前目标窗口dpi及其dpi感知级别：",end='')
        config.dst_dpi,config.dst_a = get_system_dpi(config.yys_window_hwnd)
        print(config.dst_dpi,config.dst_a)
        print("当前窗口dpi及其dpi感知级别：",end='')
        config.sys_dpi,config.sys_a = get_system_dpi(0)
        print(config.sys_dpi,config.sys_a)

        # img_x,img_y = 1180,702
        # img_x,img_y = img_x + int(22/dpi),img_y + int((45+2+10)/dpi)# 769 462 # dpi为 1.5 时，等比放大后即为 1131 636
        # init_x,init_y = 754,424 # 预设画面宽高
        if config.dst_a == -1 and config.sys_a == 0:
            mode_flag |= 4
            dpi = (config.dst_dpi*config.sys_dpi)
            config.dpi = dpi
            config.chang_x,config.chang_y = config.chang_x/dpi,config.chang_y/dpi
            config.chang_x = int(config.chang_x) +1 if config.chang_x - int(config.chang_x) > 0 else int(config.chang_x)
            config.chang_y = int(config.chang_y) +1 if config.chang_y - int(config.chang_y) > 0 else int(config.chang_y)
            config.global_x = config.init_x + config.chang_x
            config.global_y = config.init_y + config.chang_y
        else:
            config.global_x = config.init_x + 22
            config.global_y = config.init_y + 57

        print("预设窗口宽高为：",config.global_x,config.global_y)
        print("初始化窗口位置...")
        init_window_pos(config.yys_window_hwnd,config.global_x,config.global_y)
        print("初始化窗口完成")

        fp = open('./yysauto.json','r',encoding='utf-8')
        yysauto_config = json.load(fp)
        fp.close()

        yys_name = yysauto_config['user']
        while True:
            if len(yys_name) != 0:
                choose = input("请确认 "+yys_name+" 是否为你的阴阳师昵称（y/n）：")
                if choose.lower() == 'y':
                    break
                elif choose.lower() == 'n':
                    yys_name = input("请手动输入阴阳师用户名称：")
                else:
                    print('请输入 y 或者 n。')
            else:
                yys_name = input("请手动输入阴阳师用户名称：")

        yysauto_config["user"] = yys_name
        if not check_user(yys_name):
            error_exit()
        
        actions = []
        for i in yysauto_config["actions"]:
            actions.append(i)

        while True:
            help(actions)
            choose = input('请选择模式：')
            if choose == '0':
                error_exit()
            elif choose == '1':# save_img
                save_img()
            elif choose == '2':# debug
                config.mode_flag |= 1
            else:
                if choose.isdigit():
                    choose = int(choose) - 3
                    action(yysauto_config["actions"][actions[choose]])
    else:
        if version_info[0] == 3:
            windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
        # else:  # in python2.x
        #     windll.shell32.ShellExecuteW(None, u"runas", unicode(executable), unicode(__file__), None, 1)
        #     pass
