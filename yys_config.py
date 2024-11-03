mode_flag = 0
dst_dpi = 0
dst_a = 0
sys_dpi = 0
sys_a = 0
yys_window_hwnd = 0
global_x = 0
global_y = 0
chang_bordering,chang_top = 7,23# 22,57
init_x,init_y = 752,424

# huijuan = [0,0,0]
score = 0
score_list = [0,0,0] # 绘卷掉落
image = None
tupo_ticket = 0 # 突破票
state = 0 # 战斗状态：0、检测场所是否对应；1、检测战斗目标；2、是否正在战斗；3、战斗结果
step = 0 # 当前行为模式：0、回到探索界面；1、获取突破票数量；2、突破直到次数用尽；3、k28
location = 0 # 0、探索界面；1、k28进入页面；2、k28内界面；3、突破页面; 4、战斗页面; 5、结算页面
click_number = 1
tupo_attack_number = 0
tupo_exit = 0

k28_state = 0

pos_obj_list = ['again-attack', 'attack-exit', 'auto-logo', 'buff-logo', 'common-blue-exit', 'common-box-confirm', 'common-red-cancel', 'common-red-exit', 'common-yellow-confirm', 'e-mail', 'failed-logo', 'flame', 'goxie-accept', 'goxie-logo', 'goxie-refuse', 'huijuan-big', 'huijuan-normal', 'huijuan-small', 'k28-box-big', 'k28-box-small', 'k28-success-box', 'ready', 'realm-again', 'realm-logo', 'realm-success', 'realm-ticket', 'realm-wait', 'royal-logo', 'shiki-dir', 'soul-logo', 'success-damo', 'willpower', 'world-message']
k28_pos_list = ['tansuo_combat', 'tansuo_damo', 'tansuo_jinbi', 'tansuo_jingyan']
tmp_num = 0.0
obj_list = {}
for i in pos_obj_list:
    obj_list[i] = tmp_num
    tmp_num += 1.0
pos_obj = obj_list.copy()
tmp_num = 0.0
obj_list = {}
for i in k28_pos_list:
    obj_list[i] = tmp_num
    tmp_num += 1.0
k28_obj = obj_list.copy()