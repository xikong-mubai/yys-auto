from yys_windows import ctypes,win32gui,win32ui,win32con,win32api,win32process\
    ,sleep,array,check_child_windows,get_windows, Image
# 获取权限
from sys import exit
from os import system
from socket import socket
from random import randint
import yys_config
from base64 import b64encode
from io import BytesIO
from requests import post

yys_window_name = "阴阳师-网易游戏"
tempimg_name = "123.png"

def help(actions:list):
    print('1. 更新本地对比图片')
    print('2. 选择模式（默认PC端）')
    print('3. 尝试绘卷')
    for i in range(len(actions)):
        print(str(i+4) + '. ' + actions[i])
    print('0. 退出')

def update():
    version_fd = open('./version','r')
    version = version_fd.read()
    version_fd.close()
    s = socket()
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
                print("本次选择放弃升级")
            else:
                print('非法输入，默认放弃升级')
    except Exception as e:
        print(e)
        print('检测新版本失败，默认运行现有版本')
    s.close()

def flag_choose():
    print('1. 输出调试用信息')
    print('2. 使用模拟器登录')
    print('3. 待定')
    print('0. 返回')
    flag = input("请选择：")
    if not flag.isdecimal():
        print("未知输入默认返回")
    elif flag == '1':
        yys_config.flag |= 1
    elif flag == '2':
        yys_config.flag |= 2
        windows = check_child_windows(yys_config.yys_window_hwnd)
        print(windows)
        yys_config.yys_click_window = windows[1][0][0]

def error_exit():
    input("输入任意键退出")
    exit()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print('\r\n',e)
        return False

# 生成随机数
def rand_num(x:int, y:int):
    return round(randint(x, y),3)

def check_user(user_name:str):
    s = socket()
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

def mouse_click(window_hwnd,position:list):
    x_left,x_right,y_left,y_right = position
    x=rand_num(int(x_left * yys_config.global_x),int(x_right * yys_config.global_x))
    y=rand_num(int(y_left * yys_config.global_y),int(y_right * yys_config.global_y))
    if yys_config.flag % 2 == 1:
        print("\n点击位置：",x,y)
    try:
        # 推算位置 x += config.chang_bordering + 1
        # y += config.chang_top + 1
        # if yys_config.flag % 2 == 1:
        #     print(x,y)
        win32api.SendMessage(window_hwnd,win32con.WM_LBUTTONDOWN,0,(y << 16)+x)
        win32api.SendMessage(window_hwnd,win32con.WM_LBUTTONUP,0,(y << 16)+x)
    except Exception as e:
        print(e)
    #sleep(0.1)


def get_img_pixel_list(img:Image.Image,check_area:list):
    img_pixel_list = []
    x,y = img.size
    x_1 = int(x * check_area[0])
    x_2 = int(x * check_area[1])
    y_1 = int(y * check_area[2])
    y_2 = int(y * check_area[3])
    x = 0 ; sum_x = (x_2 - x_1)//9
    while x < x_2:
        if x == 0:
            x = x_1
        y = 0 ; sum_y = (y_2-y_1)//9
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
    tmp_len = len(tmp_pixel_list) if len(tmp_pixel_list) < len(dst_pixel_list) else len(dst_pixel_list)
    for i in range(tmp_len):
        pixel_sum[0] += abs(tmp_pixel_list[i][0] - dst_pixel_list[i][0])
        pixel_sum[1] += abs(tmp_pixel_list[i][1] - dst_pixel_list[i][1])
        pixel_sum[2] += abs(tmp_pixel_list[i][2] - dst_pixel_list[i][2])
    pixel_sum[0] /= tmp_len
    pixel_sum[1] /= tmp_len
    pixel_sum[2] /= tmp_len
    # 判断颜色近似度
    if yys_config.flag %2 ==1:
        print(pixel_sum)
    if pixel_sum[0] <= 6 and pixel_sum[0] >= 0 and pixel_sum[1] <= 6 and pixel_sum[1] >= 0 and pixel_sum[2] <= 6 and pixel_sum[2] >= 0:
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
        sleep(0.005)
        window = get_windows()
        if window != None:
            for i in action:
                if identify(dst_pixel_list[i],window,action[i]["check_area"],action[i]["check_pos"]):
                    print("\r"+action[i]["message"]+"    \t      \t      \t还剩余"+str(count)+"次\t",end='')
                    if action[i]["type"] == 0:
                        flag = 0
                    elif action[i]["type"] == 1 and flag == 0:
                        count -= 1
                        flag = 1
                    if len(action[i]["click_area"]) == 0:
                        continue
                    # 1480-1540 / 1579   762-820 / 887
                    x_left,x_right,y_left,y_right = action[i]["click_area"]
                    mouse_click(yys_config.yys_click_window,[x_left,x_right,y_left,y_right])
                    sleep(0.3)


def get_tickets(image):
    image_data = BytesIO()
    image.save(image_data,"png")
    tupo_ticket = 0
    data = {
        "base64": b64encode(image_data.getvalue()).decode(),
        "options": {
            "ocr.language": "models/config_chinese.txt",
            "ocr.cls": 'true',
            "ocr.limit_side_len": 4320,
            "tbpu.parser": "multi_none",
            "data.format": "text"
        }
    }
    for _ in range(5):
        r_result = post("http://127.0.0.1:1224/api/ocr",json=data)
        if r_result.status_code == 200:
            result_message = r_result.json()
            if result_message["code"] == 100:
                for i in r_result.content.split(b' '):
                    if b'/30' in i:
                        tmp_num = i.split(b'/30')[0][-2:]
                        if len(tmp_num) == 2:
                            if tmp_num[0] > 47 and tmp_num[0] < 58:
                                tupo_ticket = int(tmp_num.decode())
                            else:
                                tupo_ticket = tmp_num[1] - 48
                        else:
                            tupo_ticket = tmp_num[0]-48
                        break
                break
    else:
        print("图像识别未检测到突破票，请检查问题")
        return False,tupo_ticket
    return True,tupo_ticket