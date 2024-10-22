from ultralytics import YOLOv10
from util import get_windows,mouse_click,sleep
from requests import post
from base64 import b64encode
import config,io

model_k28 = YOLOv10("./models/k28.pt")
model_tupo = YOLOv10('./models/best.pt')
pos_obj = config.pos_obj

def click_xy(xy):
    xy = [xy[0]+0.01,xy[2]-0.01,xy[1]+0.01,xy[3]-0.01]
    print(xy)
    mouse_click(config.yys_window_hwnd,xy)

def tupo_dedup(tmp_xyxy_a,tmp_xyxy_b):
    '''清除突破中与另两种重复的框框'''
    xyxy_a = [] ; xyxy_b = tmp_xyxy_b.copy()
    for i in tmp_xyxy_a:
        flag = 0 ; tmp_xyxy = 0
        tmp_x,tmp_y = i[:2]
        for j in tmp_xyxy_b:
            x_real = tmp_x - j[0] ; y_real = tmp_y - j[1]
            if (x_real >= -0.01 and x_real <= 0.01) and (y_real >= -0.01 and y_real <= 0.01):
                flag = 1
                tmp_xyxy = j
                break

        if flag == 1:
            tmp_xyxy_b.remove(tmp_xyxy)
        else:
            xyxy_a.append(i)

    return xyxy_a,xyxy_b

def _self_dedup(tmp_a):
    '''清除数组内的重复坐标'''
    a = []
    for i in tmp_a:
        tmp_x,tmp_y = i[:2]
        for j in a:
            x_real = tmp_x - j[0] ; y_real = tmp_y - j[1]
            if (x_real >= -0.01 and x_real <= 0.01) and (y_real >= -0.01 and y_real <= 0.01):
                break
        else:
            a.append(i)
    return a

def self_dedup(r):
    '''清除识别结果中同类型的重复框框'''
    r_cls_list = r.boxes.cls.tolist()
    r_xyn_list = r.boxes.xyxyn
    tmp_r = {float(i):[] for i in range(33)}
    for i in range(len(r_cls_list)):
        tmp_r[r_cls_list[i]].append(r_xyn_list[i].tolist())
    
    r = tmp_r.copy()
    for r_item in tmp_r:
        if len(tmp_r[r_item]) == 0:
            r.pop(r_item)
        else:
            r[r_item] = _self_dedup(tmp_r[r_item])

    return r


def check(image):
    if config.location == 2:
        for _ in range(6):
            result = model_k28(image,imgsz=640,conf=0.25)
            for r in result:
                real_r = r.boxes.cls.tolist()
                if len(real_r) != 0:
                    return True,"in k28 page",r
            click_xy([0.90,0.66,0.95,0.72])
        return True,"no things",None

    result = model_tupo(image,imgsz=640,conf=0.25)
    for r in result:
        # print(r.names)
        # print(r.boxes.cls)
        # print(r.boxes.xyxy)
        real_r = r.boxes.cls.tolist()
        # if 42.0 in real_r or 39.0 in real_r: # 39: 困28；42: 突破按钮
        if (pos_obj['realm-logo'] in real_r or pos_obj['k28-box-small'] in real_r) and pos_obj['buff-logo'] in real_r:
            return True,"in TanSuo Root",r
        # elif 35.0 in real_r or 34.0 in real_r: # 35: 已攻破；34: 未攻破
        elif pos_obj['common-red-cancel'] in real_r: # 红色取消
            return True,"attack exit or tupo fresh",r
        elif pos_obj['success-damo'] in real_r:
            return True,'maybe attack success page',r
        elif pos_obj['realm-success'] in real_r or pos_obj['realm-again'] in real_r or pos_obj['realm-wait'] in real_r: # 35: 已攻破；34: 未攻破
            if pos_obj['common-box-confirm'] in real_r or real_r.count(pos_obj['common-yellow-confirm']) == 2 or real_r.count(pos_obj['realm-ticket']) == 2:
                return True, "in tupo confirm page",r
            return True,"in tupo choose page",r
        elif pos_obj['common-box-confirm'] in real_r or real_r.count(pos_obj['realm-ticket']) == 2:
            return True, "in tupo confirm page",r
        # elif 23.0 in real_r: # 红色取消
        # elif 21.0 in real_r: # 21: 黄色确认按钮 common-btn-yellow_confirm
        elif pos_obj['k28-box-big'] in real_r:
            return True,"k28 enter",r
        elif pos_obj['common-yellow-confirm'] in real_r: # 21: 黄色确认按钮 common-btn-yellow_confirm
            # if 25.0 in real_r: # 25: 红色关闭按钮
            if pos_obj['common-red-exit'] in real_r: # 25: 红色关闭按钮
                return True,"k28 enter or tupo choose",r
            # if 19.0 in real_r: # 蓝色退出按钮
            if pos_obj['common-blue-exit'] in real_r: # 蓝色退出按钮
                return True,"in k28",r
            print('\a',end='')
            print('\a',end='')
            print('\a',end='')
            return True,"maybe tupo choose or k28 exit or k28 enter",r
        # elif 5.0 in real_r: # 自动战斗标志
        elif pos_obj['auto-logo'] in real_r: # 自动战斗标志
            return True,"attacking",r
        elif pos_obj['failed-logo'] in real_r:
            return True,"failed",r
        elif pos_obj['attack-exit'] in real_r:
            return True,'attack page',r
    # result = model_youshuofa(image,imgsz=640,conf=0.1)
    # for r in result:
    #     real_r = r.boxes.cls.tolist()
    #     if 42.0 in real_r or 39.0 in real_r: # 39: 困28；42: 突破按钮
    #         return True,"in TanSuo Root",r
    click_xy([0.0065,0.62635,0.0295,0.6695])
    return False,"uknown position",None


def identify():
    image = get_windows(config.yys_window_hwnd)
    result,message,r = check(image) # 判断当前画面并返回结果
    print("----------",message,"----------")
    if result: # 未识别到突破或者k28页面
        r = self_dedup(r)
    return result,message,r


def k28_attack():
    print("no warning")



def tupo_pos_check(r):
    # attack_indexes = r.boxes.cls.tolist()
    # attack_poses = r.boxes.xyxyn.tolist()
    # tmp_xyxy_wait = [] ; tmp_xyxy_success = [] ; tmp_xyxy_again = []
    # for i in range(len(attack_indexes)):
    #     # if attack_indexes[i] == 35.0:
    #     if attack_indexes[i] == pos_obj['realm-success']:
    #         tmp_xyxy_success.append(attack_poses[i])
    #     # elif attack_indexes[i] == 34.0:
    #     elif attack_indexes[i] == pos_obj['realm-again']:
    #         tmp_xyxy_again.append(attack_poses[i])
    #     elif attack_indexes[i] == pos_obj['realm-wait']:
    #         tmp_xyxy_wait.append(attack_poses[i])

    # tmp_xyxy_wait = self_dedup(tmp_xyxy_wait)
    # tmp_xyxy_again = self_dedup(tmp_xyxy_again)
    # tmp_xyxy_success = self_dedup(tmp_xyxy_success)

    tmp_xyxy_wait = r[pos_obj['realm-wait']] if pos_obj['realm-wait'] in r.keys() else []
    tmp_xyxy_again = r[pos_obj['realm-again']] if pos_obj['realm-again'] in r.keys() else []
    tmp_xyxy_success = r[pos_obj['realm-success']] if pos_obj['realm-success'] in r.keys() else []

    xyxy_wait,xyxy_success = tupo_dedup(tmp_xyxy_wait,tmp_xyxy_success)
    xyxy_again,xyxy_success = tupo_dedup(tmp_xyxy_again,xyxy_success)
    xyxy_wait,xyxy_again = tupo_dedup(xyxy_wait,xyxy_again)

    return xyxy_wait+xyxy_again,xyxy_success


def tupo_attack(xy):
    tupo_state = 0
    while True:
        result,message,r = identify()
        if not result: # 未识别到突破或者k28页面
            continue

        if tupo_state == 0:    
            click_xy([(xy[2] - xy[0])/2,xy[1],xy[2],xy[3]])
            tupo_state += 1
        elif tupo_state == 1:
            if 'tupo confirm' in message:
                confirm_list = r[pos_obj['common-yellow-confirm']]
                tmp_count = len(confirm_list)
                if tmp_count == 1:
                    enter(r,6)
                elif tmp_count == 0 or tmp_count > 2:
                    print('\a未能检测到突破目标的进攻按钮/进攻按钮识别数量异常可能遇到问题')
                else:
                    confirm_xy = [0,0,1,0]
                    for i in confirm_list:
                        if i[2] - i[0] <= confirm_xy[2] - confirm_xy[0]:
                            confirm_xy = i
                    click_xy(confirm_xy)
            elif 'attack' in message:
                tupo_state += 1
            elif "tupo fresh" in message:
                enter(r,6)
                tupo_state = 0
            elif "tupo choose" in message:
                tupo_state = 0
        elif tupo_state == 2:
            if config.tupo_attack_number >= 9:
                click_xy([30,30,50,50])
                tupo_state += 2
            else:
                tupo_state += 1
                # config.tupo_attack_number += 1
                # return True
        elif tupo_state == 3:
            if 'attack success' in message:
                # 读取绘卷或突破票
                click_xy([0.0065,0.62635,0.0295,0.6695])
                return True
            elif 'attacking' in message:
                continue
        elif tupo_state == 4:
            if 'exit' in message:
                enter(r,6)
                config.tupo_exit += 1
                tupo_state = 0
                if config.tupo_exit >= 4:
                    config.tupo_attack_number = 0
                    config.tupo_exit = 0
                return False
            else:
                click_xy([30,30,50,50])


def tupo():
    while config.tupo_ticket > 0:
        result,message,r = identify() # 判断当前位置
        if not result or 'tupo choose' not in message: # 未识别到突破或者k28页面
            continue
        elif "attack success" in message:
            click_xy([0.0065,0.62635,0.0295,0.6695])
            continue
        xyxy_normal,xyxy_ptr = tupo_pos_check(r)
        length = len(xyxy_normal)
        if len(xyxy_ptr) + length != 9:
            print('\a',end='')
            print('\a',end='')
            print('\a',end='')
            print("未能识别够九个突破目标,可能需要手工确认")

        i = 0
        while True:
            xy = xyxy_normal[i]
            if tupo_attack(xy):
                i += 1
                config.tupo_ticket -= 1
            else:
                break

def backRoot(r):
    real_r:list[float] = r.keys()
    xy = [0.0065,0.62635,0.0295,0.6695]
    if config.click_number % 3 == 0:
        if pos_obj['common-yellow-confirm'] not in real_r:
            print("\a似乎卡住了了呢")
            sleep(100)
        else:
            xy = [0,0,0,0]
            for i in r[pos_obj['common-yellow-confirm']]:
                    if i[0] > xy[0]:
                        xy = i
            click_xy(xy)
            config.click_number += 1

    if pos_obj['common-red-exit'] in real_r:
        xy = r[pos_obj['common-red-exit']][0]
    elif pos_obj['common-blue-exit'] in real_r:
        xy = r[pos_obj['common-blue-exit']][0]
    click_xy(xy)
    config.click_number += 1

def enter(r,location):
    real_r:list[float] = r.keys()
    xy = None
    if location == 4: # 突破按钮
        xy = r[pos_obj['realm-logo']][0]
    elif location == 6: # 非刷新或者退出的黄色按钮
        if pos_obj['common-red-cancel'] in real_r:
            xy = r[pos_obj['common-red-cancel']][0]
        else:
            xy = r[pos_obj['common-yellow-confirm']][0]
    elif location == 7: # 最右侧的黄色
        if len(r[pos_obj['common-yellow-confirm']]) != 0:
            xy = [0,0,0,0]
        for i in r[pos_obj['common-yellow-confirm']]:
            if i[0] >= xy[0]:
                xy = i
    if xy != None:
        click_xy(xy)

def get_tickets(image_data):
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
                        config.tupo_ticket = int(i.split(b'/30')[0][-2:].decode())
                        break
                break
    else:
        print("图像识别未检测到突破票，请检查问题")
        return False
    return True

def huijuan():
    # global config.score_list,config.click_number,config.tupo_ticket,config.step,locatio
    config.tupo_ticket = 0 # 突破票
    config.step = 0 # 当前行为模式：0/3、回到探索界面；1、获取突破票数量；2、突破直到次数用尽；4、k28
    location = 0 # 0、探索界面；1、k28进入页面；2、k28内界面；3、k28退出；4、突破页面;5、突破确认目标页面；6、战斗页面
    real_score = 100 * config.score_list[0] + 20 * config.score_list[1] + 10 * config.score_list[2]
    while real_score < config.score:
        image = get_windows(config.yys_window_hwnd)
        result,message,r = check(image) # 判断当前位置
        if not result: # 未识别到突破或者k28页面
            continue
        
        r = self_dedup(r)
        if config.step == 0 or 3 == config.step:
        # 返回探索页
            config.click_number = 1
            if 'Root' not in message:
                backRoot(r)
                continue
            config.step += 1
        elif config.step == 1:
        # 获取突破剩余次数
            image_data = io.BytesIO()
            image.save(image_data,"png")
            if not get_tickets(image_data):
                continue
            if config.tupo_ticket > 0:
                config.step += 1
            else:
                config.step += 2
        elif config.step == 2:
        # 突破
            enter(r,4)
            tupo()
            config.step += 1
        elif config.step == 4:
        # k28直到突破票满
            k28_attack()
            config.step = 0
            