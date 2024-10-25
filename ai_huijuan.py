from ultralytics import YOLOv10
from yys_util import get_windows,mouse_click,sleep
from requests import post
from base64 import b64encode
from io import BytesIO
import yys_config

# location : 0、探索界面；1、k28进入页面；2、k28内界面；3、突破页面; 4、战斗页面; 5、结算页面
location_codes = {
    'tansuo':0, "k28_box":1,"k28":2,"tupo":3,"attack":4,"settlement":5
}
# step ：0、回到探索界面；1、获取突破票数量；2、突破直到次数用尽；3、k28
step_codes = {
    "go_tansuo":0, "get_tickets":1, "tupo":2, "k28":3,
}
# state ：0、检测场所是否对应；1、检测战斗目标；2、是否正在战斗；3、战斗结果
state = {
    "location_check":0, "choose":1, "attack":2, "Settlement":3
}

global model_k28,model_tupo
def model_init():
    global model_k28,model_tupo
    print("初始化AI模型...")
    try:
        model_k28 = YOLOv10("./models/k28.pt")
        model_tupo = YOLOv10('./models/last.pt')
        print("初始化成功")
    except Exception as e:
        print("模型加载出现问题：",e)
pos_obj = yys_config.pos_obj

def click_xy(xy):
    xy = [xy[0]+0.01,xy[2]-0.01,xy[1]+0.01,xy[3]-0.01]
    print(xy)
    mouse_click(yys_config.yys_window_hwnd,xy)

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
    '''清除数组内的重复框框'''
    a = []
    for i in tmp_a:
        a_copy = a.copy()
        for j in a_copy:
            x_real = i[0] - j[0] ; y_real = i[1] - j[1]
            if (x_real >= -0.01 and x_real <= 0.01) and (y_real >= -0.01 and y_real <= 0.01):
                x_real = i[2] - i[0] ; y_real = i[3] - i[1] ; x_tmp = j[2] - j[0] ; y_tmp = j[3] - j[1]
                x_real -= x_tmp ; y_real -= y_tmp
                if x_real > 0 or y_real > 0 :
                    a[a.index(j)] = i
                # elif x_real <= -0.05 or y_real <= -0.05:  
                break
        else:
            a.append(i)
        a_copy.clear()
    return a

def self_dedup(r):
    '''清除识别结果中同类型的重复框框以及未识别到内容的类型'''
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

def k28_check(image):
    for _ in range(6):
        try:
            result = model_k28(image,imgsz=640,conf=0.25)
        except Exception as e:
            print("模型识别遇到问题",e)
            return False,e,None
        for r in result:
            real_r = r.boxes.cls.tolist()
            if len(real_r) != 0:
                return True,"in k28 page",r
        click_xy([0.90,0.66,0.95,0.72])
    return True,"no things",None

def no_k28_check(image):
    # if yys_config.location == 2:
    #     return k28_check(image)
    try:
        result = model_tupo(image,imgsz=640,conf=0.25)
    except Exception as e:
        print("模型识别遇到问题",e)
        return False,e,None
    for r in result:
        # print("似乎识别到了呢")
        # print(r.names)
        # print(r.boxes.cls)
        # print(r.boxes.xyxy)
        real_r = r.boxes.cls.tolist()
        if pos_obj['common-blue-exit'] in real_r and pos_obj['shiki-dir'] in real_r:
            return True,"in k28",r
        # if 42.0 in real_r or 39.0 in real_r: # 39: 困28；42: 突破按钮
        if (pos_obj['realm-logo'] in real_r or pos_obj['k28-box-small'] in real_r) and pos_obj['buff-logo'] in real_r:
            return True,"in TanSuo Root",r
        # elif 35.0 in real_r or 34.0 in real_r: # 35: 已攻破；34: 未攻破
        elif pos_obj['common-red-cancel'] in real_r: # 红色取消
            return True," exit or tupo fresh",r
        elif pos_obj['success-damo'] in real_r:
            return True,'maybe success page',r
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
            # if 25.0 in real_r: # 25: 红色退出按钮
            if pos_obj['common-red-exit'] in real_r: # 25: 红色退出按钮
                return True,"k28 enter or tupo choose",r
            # if 19.0 in real_r: # 蓝色退出按钮
            if pos_obj['common-blue-exit'] in real_r: # 蓝色退出按钮
                return True,"maybe k28",r
            print('\a',end='')
            print('\a',end='')
            print('\a',end='')
            return True,"maybe tupo choose or k28 exit or k28 enter",r
        # elif 5.0 in real_r: # 自动战斗标志
        elif pos_obj['auto-logo'] in real_r: # 自动战斗标志
            return True,"attacking",r
        elif pos_obj['failed-logo'] in real_r:
            return True,"failed",r
        elif pos_obj['ready'] in real_r:
            return True,'attack page',r
        elif pos_obj['attack-exit'] in real_r:
            return True,'attack page',r
    # result = model_youshuofa(image,imgsz=640,conf=0.1)
    # for r in result:
    #     real_r = r.boxes.cls.tolist()
    #     if 42.0 in real_r or 39.0 in real_r: # 39: 困28；42: 突破按钮
    #         return True,"in TanSuo Root",r
    click_xy([0.0065,0.62635,0.0295,0.6695])
    return False,"uknown position",None

def location_change(message):
    if yys_config.location == location_codes['tansuo']:
        if 'k28' in message:
            yys_config.location = location_codes['k28_box']
        elif 'tupo' in message:
            yys_config.location = location_codes['tupo']
    elif yys_config.location == location_codes['k28_box']:
        if 'in k28' in message:
            yys_config.location = location_codes['k28']
        elif 'Root' in message:
            yys_config.location = location_codes['tansuo']
    elif yys_config.location == location_codes['k28']:
        if 'k28 enter' in message:
            yys_config.location = location_codes['k28_box']
        elif 'attack' in message:
            yys_config.location = location_codes['attack']
    elif yys_config.location == location_codes['attack']:
        if 'success' in message or 'failed' in message:
            yys_config.location = location_codes['settlement']
        elif 'tupo' in message:
            yys_config.location = location_codes['tupo']
        elif 'k28' in message:
            yys_config.location = location_codes['k28']
    elif yys_config.location == location_codes['settlement']:
        if 'tupo' in message:
            yys_config.location = location_codes['tupo']
        elif 'in k28' in message:
            yys_config.location = location_codes['k28']
        elif 'k28' in message:
            yys_config.location = location_codes['k28_box']
    else:
        if 'Root' in message:
            yys_config.location = location_codes['tansuo']
        elif 'attack' in message:
            yys_config.location = location_codes['attack']

def identify():
    image = get_windows(yys_config.yys_window_hwnd)
    if yys_config.location == 2 and yys_config.step == 3:
        result,message,r = k28_check(image) # 判断当前画面并返回结果
    else:
        result,message,r = no_k28_check(image) # 判断当前画面并返回结果
    print("----------",message,"----------")
    if result: # 未识别到突破或者k28页面
        r = self_dedup(r)
        location_change(message)
    return result,message,r,image


def k28_attack(result,message,r,image):
    print("no warning")


def tupo_pos_check(r):
    tmp_xyxy_wait = r[pos_obj['realm-wait']] if pos_obj['realm-wait'] in r.keys() else []
    tmp_xyxy_again = r[pos_obj['realm-again']] if pos_obj['realm-again'] in r.keys() else []
    tmp_xyxy_success = r[pos_obj['realm-success']] if pos_obj['realm-success'] in r.keys() else []

    xyxy_wait,xyxy_success = tupo_dedup(tmp_xyxy_wait,tmp_xyxy_success)
    xyxy_again,xyxy_success = tupo_dedup(tmp_xyxy_again,xyxy_success)
    xyxy_wait,xyxy_again = tupo_dedup(xyxy_wait,xyxy_again)

    return xyxy_wait+xyxy_again,xyxy_success


def tupo_attack(xy):
    tupo_state = 0 ; flag = 0 ; success_flag =  0
    result,message,r,image = identify()
    while True:
        if not result: # 未识别到突破或者k28页面
            pass
        elif tupo_state == state['location_check']:
            if yys_config.location != location_codes['tupo'] and yys_config.location != location_codes['settlement'] \
                and location_codes['attack']:
                return False
            elif yys_config.location == location_codes['tupo']:
                tupo_state = state['choose']
            elif yys_config.location == location_codes['settlement']:
                click_xy([0.0065,0.62635,0.0295,0.6695])
                continue
        elif tupo_state == state['choose']:
            if flag == 0:
                click_xy([(xy[2] + xy[0])/2,xy[1],xy[2],xy[3]])
                flag = 1
            elif flag == 1:
                if yys_config.location != location_codes['tupo']:
                    flag = 0
                    tupo_state = state['attack']
                    continue
                elif pos_obj['common-red-cancel'] in r.keys():
                    flag = 0
                    enter(r,6)
                elif pos_obj['common-yellow-confirm'] in r.keys():
                    confirm_list = r[pos_obj['common-yellow-confirm']]
                    tmp_count = len(confirm_list)
                    if tmp_count == 1:
                        enter(r,6)
                    elif tmp_count == 2:
                        confirm_xy = [0,0,1,0]
                        for i in confirm_list:
                            if i[2] - i[0] <= confirm_xy[2] - confirm_xy[0]:
                                confirm_xy = i
                        click_xy(confirm_xy)
                    else:
                        print('\a按钮识别数量异常可能遇到问题')
                        click_xy([0.0065,0.62635,0.0295,0.6695])
                        flag = 0
                else:
                    print('\a未能检测到突破目标的进攻按钮')
                    click_xy([0.0065,0.62635,0.0295,0.6695])
                    flag = 0
            # tupo_state = state['attack']
        elif tupo_state == state['attack']:
            if yys_config.tupo_attack_number >= 9:
                if pos_obj['common-red-cancel'] not in r.keys():
                    click_xy([30,30,50,50])
                else:
                    enter(r,6)
            if yys_config.location != location_codes['attack']:
                tupo_state = state['Settlement']
        elif tupo_state == state['Settlement']:
            if 'success' in message:
                # 读取绘卷或突破票
                if yys_config.location == location_codes['tupo']:
                    return True
                if success_flag == 0:
                    yys_config.tupo_attack_number += 1
                    success_flag = 1
                click_xy([0.0065,0.62635,0.0295,0.6695])
            elif 'failed' in message:
                yys_config.tupo_exit += 1
                if yys_config.tupo_exit >= 4:
                    yys_config.tupo_attack_number = 0
                    yys_config.tupo_exit = 0
                click_xy([0.0065,0.62635,0.0295,0.6695])
                tupo_state = state['location_check']
        result,message,r,image = identify()


def tupo(r):
    # while yys_config.tupo_ticket > 0:
    #     result,message,r = identify() # 判断当前位置
    # if not result or 'tupo choose' not in message: # 未识别到突破或者k28页面
        
    # elif "attack success" in message:
    #     click_xy([0.0065,0.62635,0.0295,0.6695])
    #     continue
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
            yys_config.tupo_ticket -= 1
            if i == length:
                break
        else:
            break

def backRoot(r):
    real_r:list[float] = r.keys()
    xy = [0.0065,0.62635,0.0295,0.6695]
    if yys_config.click_number % 3 == 0:
        if pos_obj['common-yellow-confirm'] not in real_r:
            print("\a似乎卡住了了呢")
            sleep(100)
        else:
            xy = [0,0,0,0]
            for i in r[pos_obj['common-yellow-confirm']]:
                    if i[0] > xy[0]:
                        xy = i
            click_xy(xy)
            yys_config.click_number += 1

    if pos_obj['common-red-exit'] in real_r:
        xy = r[pos_obj['common-red-exit']][0]
    elif pos_obj['common-blue-exit'] in real_r:
        xy = r[pos_obj['common-blue-exit']][0]
    click_xy(xy)
    yys_config.click_number += 1

def enter(r,location):
    real_r:list[float] = r.keys()
    xy = None
    if location == location_codes['tupo']: # 突破按钮
        xy = r[pos_obj['realm-logo']][0]
    elif location == location_codes['k28_box']:
        xy = [0,0,0,0]
        for i in r[pos_obj['k28-box-small']]:
            if i[1] > xy[1]:
                xy = i
        else:
            xy = None
    elif location == location_codes['tansuo']:
        backRoot(r)
        return
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
    else:
        print('未能找到想要进入的场景入口按钮，继续尝试...')

def get_tickets(image):
    image_data = BytesIO()
    image.save(image_data,"png")
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
                                yys_config.tupo_ticket = int(tmp_num.decode())
                            else:
                                yys_config.tupo_ticket = tmp_num[1] - 48
                        else:
                            yys_config.tupo_ticket = tmp_num[0]-48
                        break
                break
    else:
        print("图像识别未检测到突破票，请检查问题")
        return False
    return True

def huijuan():
    # global config.score_list,config.click_number,config.tupo_ticket,config.step,locatio
    yys_config.tupo_ticket = 0 # 突破票
    yys_config.step = 0 # 当前行为模式：0/3、回到探索界面；1、获取突破票数量；2、突破直到次数用尽；4、k28
    real_score = 100 * yys_config.score_list[0] + 20 * yys_config.score_list[1] + 10 * yys_config.score_list[2]
    model_init()
    result,message,r,image = identify() # 判断当前位置
    while real_score < yys_config.score:
        print("\r 当前记录分数：",real_score)
        if not result: # 未识别到突破或者k28页面
            pass
        elif yys_config.step == 0:# or 3 == yys_config.step:
        # 返回探索页
            yys_config.click_number = 1
            if yys_config.location != location_codes['tansuo']:
                enter(r,location_codes['tansuo'])
            else:
                yys_config.step += 1
                continue
        elif yys_config.step == 1:
        # 获取突破剩余次数
            if not get_tickets(image):
                print("突破票初始化失败，再次尝试。。。")
            if yys_config.tupo_ticket > 0:
                enter(r,location_codes['tupo'])
                yys_config.step += 1
            else:
                enter(r,location_codes['k28_box'])
                yys_config.step += 2
        elif yys_config.step == 2:
        # 突破
            if yys_config.location != location_codes['tupo'] and yys_config.location != location_codes['settlement'] \
                and location_codes['attack']:
                yys_config.step = 0
            elif yys_config.tupo_ticket > 0:
                tupo(r)
                if yys_config.location == location_codes['k28_box'] or yys_config.location == location_codes['tupo'] \
                    or yys_config.location == location_codes['tansuo']:
                    get_tickets(image)
                # print("突破票初始化失败，再次尝试。。。")
            else:
                yys_config.step = 0
        elif yys_config.step == 3:
        # k28直到突破票满
            if yys_config.location == location_codes['tansuo'] and yys_config.location == location_codes['tupo']:
                yys_config.step = 0
            elif yys_config.tupo_ticket < 30:
                k28_attack(result,message,r,image)
                if yys_config.location == location_codes['k28_box'] or yys_config.location == location_codes['tupo'] \
                    or yys_config.location == location_codes['tansuo']:
                    get_tickets(image)
            else:
                yys_config.step = 0
        result,message,r,image = identify() # 判断当前位置