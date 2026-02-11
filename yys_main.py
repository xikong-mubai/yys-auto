# 获取权限
# from ctypes import windll
import yys_config,json
from yys_util import get_windows,flag_choose, \
help,check_user,error_exit,update,action
from yys_windows import check_windows,get_system_dpi,init_window_pos,\
    init_capture_handle
from yys_huijuan import huijuan
from yys_huijuan_fsm import GameEngine  # <--- 导入新模块

def save_img():
    num = 0
    while True:
        choose = input("请将游戏运行至想要截取的画面，然后输入 1 进行画面截取。输入 0 返回主菜单")
        if choose == '0':
            return
        elif choose == '1':
            window = get_windows()
            if window != None:
                window.save('./img/tmp_'+str(num)+".png")
                num += 1
                window.close()
            else:
                print("本次获取失败")

def get_window_handle():
    # 为空会获取到资源管理器的子窗口pid（空窗口）
    result,windows = check_windows()
    if not result:
        error_exit()
    return windows

def choose_windows(windows):
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
                    raise ValueError("序号输入错误")
                break
            except Exception as e:
                print(e)
    yys_config.yys_window_hwnd = windows[choose][0]
    yys_config.yys_click_window = windows[choose][0]
    yys_config.yys_window_xy = windows[choose][3]
    init_capture_handle(windows[choose][0])

def dpi_init():
    print("当前目标窗口dpi及其dpi感知级别：",end='')
    yys_config.dst_dpi,yys_config.dst_a = get_system_dpi(yys_config.yys_window_hwnd)
    print(yys_config.dst_dpi,yys_config.dst_a)
    print("当前系统dpi及其dpi感知级别：",end='')
    yys_config.sys_dpi,yys_config.sys_a = get_system_dpi(0)
    print(yys_config.sys_dpi,yys_config.sys_a)

def position_init(huijuan_flag):
    # img_x,img_y = 1180,702
    # img_x,img_y = img_x + int(22/dpi),img_y + int((45+2+10)/dpi)# 769 462 # dpi为 1.5 时，等比放大后即为 1131 636
    # init_x,init_y = 752,424 #754,424 # 预设画面宽高
    dpi = (yys_config.dst_dpi*yys_config.sys_dpi)
    yys_config.dpi = dpi
    dpi = 1.5 if dpi == 1 and huijuan_flag == 1 else 1
    yys_config.global_x =  yys_config.init_x * dpi ; yys_config.global_y = yys_config.init_y * dpi
    yys_config.global_x = int(yys_config.global_x) ; yys_config.global_y = int(yys_config.global_y)
    # # config.chang_bordering = int(config.chang_bordering) +1 if config.chang_bordering - int(config.chang_bordering) > 0 else int(config.chang_bordering)
    # # config.chang_top = int(config.chang_top) +1 if config.chang_top - int(config.chang_top) > 0 else int(config.chang_top)
    # yys_config.chang_bordering,yys_config.chang_top = int(yys_config.chang_bordering*yys_config.dpi),int(yys_config.chang_top*yys_config.dpi)
    # yys_config.global_x = yys_config.init_x + yys_config.chang_bordering * 2 + 2
    # yys_config.global_y = yys_config.init_y + yys_config.chang_top + yys_config.chang_bordering * 2 + 2
    # print("预设窗口宽高为：",yys_config.global_x,yys_config.global_y)
    print("初始化窗口位置(size: ",yys_config.global_x,yys_config.global_y,")...")
    init_window_pos(yys_config.yys_window_hwnd,yys_config.global_x,yys_config.global_y,
                    yys_config.yys_window_xy[0],yys_config.yys_window_xy[1])
    print("初始化窗口完成")

def main():
    update()
    print("请稍等，正在加载资源......")

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

    windows = get_window_handle()
    choose_windows(windows)
    dpi_init()

    while True:
        help(actions)
        choose = input('请选择模式：')

        if choose == '0':
            error_exit()
        elif choose == '1':# save_img
            save_img()
        elif choose == '2':# debug
            flag_choose()
        elif choose == '3':# 绘卷
            position_init(1)
            score = input("请输入今日目标绘卷分数（0-2000）：").strip()
            try:
                score = int(score)
                if score < 0 or score >= 2000:
                    raise ValueError("序号输入错误")
            except Exception as e:
                print(e)
            yys_config.score = score
            
            # --- 【修改点】启动新的状态机 ---
            print("正在启动新版 FSM 引擎...")
            engine = GameEngine()
            engine.start() # 这是一个阻塞的死循环，直到按 Ctrl+C
            
            # 原有的调用注释掉
            # huijuan() 
        else:
            position_init(0)
            if choose.isdigit():
                choose = int(choose) - 4
                action(yysauto_config["actions"][actions[choose]])