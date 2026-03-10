# -*- coding: utf-8 -*-
import time
from abc import ABC, abstractmethod
from ultralytics import YOLOv10

# 引入原有项目依赖
import yys_config
from yys_util import get_windows, mouse_click, sleep, get_tickets
from yys_windows import release_capture

# ==============================================================================
# 1. 上下文管理器 (Context) - 核心资源与数据总线
# ==============================================================================
class GameContext:
    def __init__(self):
        self.running = True
        # --- 模型资源 ---
        self.model_k28 = None
        self.model_general = None
        
        # 运行时数据
        self.current_image = None
        self.yolo_results = None  # 缓存最近一次识别结果
        self.frame_id = 0         # 逻辑帧计数器
        # self.pre_ctx = None
        
        # 统计数据
        self.loop_count = 0       # 刷本次数
        self.target_count = 0     # 目标次数 (从配置读或输入)
        self.situation = 0         # 场景标记：0，k28；1，突破
        self.move_count = 0 ; self.k28_exit_flag = 0    # k28移动次数；k28退出标记
        self.realm_tickets = 0
        self.realm_target_num = 0 ; self.realm_exit_count = 0
        
        # 加载配置中的坐标映射 (直接引用 yys_config 中的定义)
        self.pos_obj = yys_config.pos_obj
        self.k28_obj = yys_config.k28_obj

        # 初始化模型
        self._init_models()

    def _init_models(self):
        print(">>> [FSM] 正在加载 AI 模型...")
        try:
            self.model_k28 = YOLOv10("./models/k28.pt")
            self.model_general = YOLOv10('./models/best.pt') # 假设 last.pt 是通用检测
            print(">>> [FSM] 模型加载完成")
        except Exception as e:
            print(f">>> [错误] 模型加载失败: {e}")
            self.running = False

    def update_screen(self, timeout=1.0):
        """
        [极速版] 尝试获取最新画面。
        如果获取到了，返回 True；如果没有新画面（DLL没回调），返回 False。
        绝对不 Sleep。
        """
        img = get_windows() # 这里返回的是 numpy array
        if img is not None:
            self.current_image = img
            self.frame_id += 1
            return True
        return False
    
    def init_k28_count(self):
        self.move_count = 0
        self.k28_exit_flag = 0



# ==============================================================================
# 2. 状态基类 (Base State)
# ==============================================================================
class BaseState(ABC):
    def __init__(self, ctx: GameContext):
        self.ctx = ctx
        self.pos_obj = ctx.pos_obj
        self.k28_obj = ctx.k28_obj
        self.last_detect_time = 0

    @abstractmethod
    def on_enter(self):
        """进入状态时触发"""
        pass

    @abstractmethod
    def execute(self):
        """
        每帧执行的逻辑
        :return: 下一个状态实例 OR self (保持当前状态)
        """
        pass

    @abstractmethod
    def on_exit(self):
        """离开状态时触发"""
        pass

    def _dedup_boxes(self, box_list):
        '''清除数组内的重复/嵌套框框'''
        if not box_list:
            return []
            
        final_boxes = []
        for i in box_list:
            # i = [x1, y1, x2, y2]
            skip_i = False
            
            # 检查 i 是否与 final_boxes 中已有的框重复
            for index, j in enumerate(final_boxes):
                # 计算左上角的坐标差
                x_diff = i[0] - j[0]
                y_diff = i[1] - j[1]
                
                # 判断阈值 (0.01) - 这里的逻辑是您原版的：如果起始点非常接近
                if (-0.01 <= x_diff <= 0.01) and (-0.01 <= y_diff <= 0.01):
                    # 进一步判断大小，保留包含更多信息的那个（或者是特定逻辑）
                    # 原版逻辑似乎是：如果重叠，检查宽高差
                    w_i = i[2] - i[0]
                    h_i = i[3] - i[1]
                    w_j = j[2] - j[0]
                    h_j = j[3] - j[1]
                    
                    diff_w = w_i - w_j
                    diff_h = h_i - h_j
                    
                    # 原版逻辑：如果 i 比 j 大 (x_real > 0)，替换 j
                    if diff_w > 0 or diff_h > 0:
                        final_boxes[index] = i
                    
                    skip_i = True
                    break
            
            if not skip_i:
                final_boxes.append(i)
                
        return final_boxes

    # --- 通用工具方法 ---
    def detect(self, model, conf=0.3, imgsz=640):
        """执行 YOLO 识别并返回去重后的 key 列表"""
        if not self.ctx.current_image:
            return {}, []
        
        try:
            # 1. 推理
            # results = model(self.ctx.current_image, imgsz=640, conf=conf, verbose=False)
            if yys_config.flag & 2 == 1:
                verbose = True
            else:
                verbose = False
            results = model(self.ctx.current_image, imgsz=imgsz, conf=conf, verbose=verbose)
            
            # 2. 简易解析 (这里暂简化了原有的 self_dedup 逻辑，优先跑通流程)
            # 返回格式： {class_id: [[x1, y1, x2, y2], ...]}
            detected_dict = {} 
            raw_results = results[0]
            
            if raw_results.boxes:
                # 先按类别归类
                tmp_dict = {}
                for box in raw_results.boxes:
                    cls_id = float(box.cls)
                    xyxyn = box.xyxyn.tolist()[0] # [x1, y1, x2, y2] 归一化坐标
                    
                    if cls_id not in tmp_dict:
                        tmp_dict[cls_id] = []
                    tmp_dict[cls_id].append(xyxyn)
                
                # 3. 对每个类别单独进行去重
                for cls_id, boxes in tmp_dict.items():
                    deduplicated_boxes = self._dedup_boxes(boxes)
                    if deduplicated_boxes:
                        detected_dict[cls_id] = deduplicated_boxes
                    
            return detected_dict, raw_results
        except Exception as e:
            print(f"[识别错误] {e}")
            return {}, []

    def find_best_click_pos(self, box_list, rule='first'):
        """
        根据策略从框列表中选择最佳点击目标
        :param box_list: 候选框列表 [[x1, y1, x2, y2], ...]
        :param rule: 策略 'first'(默认), 'left'(最左), 'right'(最右), 'center'(最中心), 'random'
        :return: 最佳框 [x1, y1, x2, y2]
        """
        if not box_list:
            return None
        
        if len(box_list) == 1 or rule == 'first':
            return box_list[0]

        if rule == 'right':
            # 返回 x1 最大的 (屏幕最右侧)
            return max(box_list, key=lambda b: b[0])
        elif rule == 'left':
            # 返回 x1 最小的 (屏幕最左侧)
            return min(box_list, key=lambda b: b[0])
        elif rule == 'top':
            # 返回 y1 最小的 (屏幕最上部)
            return min(box_list, key=lambda b: b[1])
        elif rule == 'bottom':
            # 返回 y1 最大的 (屏幕最下部)
            return max(box_list, key=lambda b: b[1])
        elif rule == 'center':
            # 返回距离屏幕中心 (0.5, 0.5) 最近的
            def dist_to_center(b):
                cx = (b[0] + b[2]) / 2
                cy = (b[1] + b[3]) / 2
                return (cx - 0.5)**2 + (cy - 0.5)**2
            return min(box_list, key=dist_to_center)

        # 默认返回第一个
        return box_list[0]
    
    def click_xy(self, xy):
        xy = [xy[0]+0.01,xy[2]-0.01,xy[1]+0.01,xy[3]-0.01]
        if xy[1] < xy[0]: tmp = xy[1] ; xy[1] = xy[0] ; xy[0] = tmp
        if xy[3] < xy[2]: tmp = xy[3] ; xy[3] = xy[2] ; xy[2] = tmp
        #print(xy)
        mouse_click(yys_config.yys_click_window,xy)


# ==============================================================================
# 3. 具体业务状态实现 (以 K28 流程为例)
# ==============================================================================

# --- 状态：探索/找怪 (对应原来的 k28 逻辑) ---
class StateExploration(BaseState):
    def on_enter(self):
        print(f"\r>>> [状态] 探索中... (已完成: {self.ctx.loop_count})", end="")
        self.k28Box_small_count = 0

    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen():
            return self # 画面获取失败，下一帧再试

        # 2. 识别 (使用 general 模型)
        res, _ = self.detect(self.ctx.model_general, conf=0.3)
        
        # 3. 决策逻辑
        #k28_combat_id = self.ctx.k28_obj.get('tansuo_combat', -1.0)
        k28_box_small = self.ctx.pos_obj.get('k28-box-small', -1.0) # 纸人小盒子
        k28_box_big = self.ctx.pos_obj.get('k28-box-big', -1.0) # 这里的 key 需要确认是否为探索界面的确认
        realm_logo = self.ctx.pos_obj.get('realm-logo', -1.0) # 突破入口
        realm_wait = self.ctx.pos_obj.get('realm-wait', -1.0) # 突破目标-等待挑战
        realm_again = self.ctx.pos_obj.get('realm-again', -1.0) # 突破目标-再次挑战
        realm_success = self.ctx.pos_obj.get('realm-success', -1.0) # 突破目标-成功

        # [场景A] 如果已经在 K28 入口 (有时候点击了但没反应过来)
        if k28_box_big in res:
             print("\n>>> 已位于k28入口，切换状态")
             return StateK28Box(self.ctx)
        # [场景B] 如果已经在突破界面 (有时候点击了但没反应过来)
        if realm_again in res or realm_wait in res or realm_success in res:
            print("\n>>> 已经进入突破列表界面，切换状态")
            return StateTupoList(self.ctx)
        # [场景C] 突破门票足够，进入突破界面
        if realm_logo in res and self.ctx.situation == 1:
            print("\n>>> 突破门票达标，进入突破")
            target = self.find_best_click_pos(res[realm_logo], rule='bottom')
            self.click_xy( target)
            # return StateTupoList(self.ctx) # 突破界面和k28入口界面很像，可以先切到k28入口的状态逻辑里再细分
        # [场景D] 发现k28入口 -> 点击 -> 进入k28入口
        if k28_box_small in res and realm_logo in res:
            self.k28Box_small_count += 1
            if self.k28Box_small_count >= 6:
                print("\n>>> 发现k28入口，点击进入")
                target = self.find_best_click_pos(res[k28_box_small], rule='bottom')
                self.click_xy( target)
                sleep(0.5) # 等待动画
                # return StateK28Box(self.ctx)
        
        return self

    def on_exit(self):
        pass


# --- 状态：突破界面 ---
class StateTupoList(BaseState):
    def _tupo_dedup(self,tmp_xyxy_a,tmp_xyxy_b):
        """
        跨类别去重逻辑：
        如果 list_a 和 list_b 中存在坐标极度接近的框，
        则从 B 中移除该框，并且也不将其加入 A 中（严格剔除争议目标）。
        """
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
    
    def _tupo_pos_check(self,r,realm_wait,realm_again,realm_success):
        '''清除突破中与另两种重复的框框'''
        tmp_xyxy_wait = r[realm_wait] if realm_wait in r else []
        tmp_xyxy_again = r[realm_again] if realm_again in r else []
        tmp_xyxy_success = r[realm_success] if realm_success in r else []

        xyxy_wait,xyxy_success = self._tupo_dedup(tmp_xyxy_wait,tmp_xyxy_success)
        xyxy_again,xyxy_success = self._tupo_dedup(tmp_xyxy_again,xyxy_success)
        xyxy_wait,xyxy_again = self._tupo_dedup(xyxy_wait,xyxy_again)

        return xyxy_wait,xyxy_again,xyxy_success

    def on_enter(self):
        print(">>> [状态] 突破界面")
        self.wait_count = 0
    
    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen():
            return self # 画面获取失败，下一帧再试

        # 2. 识别 (使用 general 模型)
        res, _ = self.detect(self.ctx.model_general, conf=0.3)
        
        # 3. 决策逻辑
        realm_wait = self.ctx.pos_obj.get('realm-wait', -1.0)
        realm_again = self.ctx.pos_obj.get('realm-again', -1.0)
        realm_success = self.ctx.pos_obj.get('realm-success', -1.0)
        wait_targets, again_targets, success_targets = self._tupo_pos_check(res,realm_wait,realm_again,realm_success)
        self.ctx.realm_target_num = len(wait_targets)+ len(again_targets)
        if self.ctx.realm_target_num + len(success_targets) < 9 and self.ctx.realm_target_num > 0:
            print(">>> 识别出现问题，建议关闭突破功能等待优化后使用...\a")

        # [场景A] 已经回到探索界面了 (有时候点击了但没反应过来)
        realm_logo = self.ctx.pos_obj.get('realm-logo', -1.0)
        if realm_logo in res:
            print(">>> 已经回到探索界面，切回探索状态")
            return StateExploration(self.ctx)
        # [场景B] 可能已经点开突破确认界面了
        confrim_id = self.ctx.pos_obj.get('common-yellow-confirm', -1.0)
        common_box_confirm = self.ctx.pos_obj.get('common-box-confirm', -1.0)
        if (confrim_id in res and common_box_confirm in res)\
            or len(res[confrim_id]) >= 2:
            print(">>> 已经进入突破确认界面")
            return StateTupoConfrim(self.ctx)
        # [场景C] 门票耗尽，回到探索界面
        id_exit = self.ctx.pos_obj.get('common-red-exit', -1.0)
        if id_exit in res:
            print(">>> 突破门票不足，回到探索界面")
            target = self.find_best_click_pos(res[id_exit], rule='right')
            self.click_xy(target)
            # sleep(1.0) # 等待动画
            # return StateExploration(self.ctx)
        # [场景D] 优先打未打过的
        if realm_wait in res:
            print(">>> 发现新目标准备进攻...")
            target = self.find_best_click_pos(res[realm_again], rule='left')
            self.click_xy(target)
            #return StateTupoConfrim(self.ctx) # 突破确认界面
        elif realm_again in res:
            print(">>> 突破界面加载完成，进入突破列表")
            target = self.find_best_click_pos(res[realm_again], rule='left')
            self.click_xy(target)
            #return StateTupoConfrim(self.ctx) # 突破列表界面
        
        return self
    
    def on_exit(self):
        pass


# --- 状态：突破确认界面 ---
class StateTupoConfrim(BaseState):
    def on_enter(self):
        print(">>> [状态] 突破进攻确认")
        
    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen():
            return self # 画面获取失败，下一帧再试

        # 2. 识别 (使用 general 模型)
        res, _ = self.detect(self.ctx.model_general, conf=0.3)
        
        # 3. 决策逻辑
        confrim_id = self.ctx.pos_obj.get('common-yellow-confirm', -1.0)
        
        # [场景A] 已经进入战斗逻辑了 (有时候点击了但没反应过来)
        if confrim_id in res:
            print(">>> 点击确认按钮")
            target = self.find_best_click_pos(res[confrim_id], rule='right')
            self.click_xy(target)
            sleep(1.0) # 等待动画
            return StateCombat(self.ctx)
        # [场景B] 点击确认，进入战斗

        return self
    
    def on_exit(self):
        pass


# --- 状态：K28 入口界面 ---
class StateK28Box(BaseState):
    def on_enter(self):
        print(">>> [状态] K28 入口界面")
        self.tansuo_count = 0
        self.k28_count = 0

    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen():
            return self # 画面获取失败，下一帧再试

        # 2. 识别 (使用 general 模型)
        res, _ = self.detect(self.ctx.model_general, conf=0.3)

        # 3. 决策逻辑
        # [场景A] 如果已经在 K28 场景 (有时候点击了但没反应过来)
        sd_id = self.ctx.pos_obj.get('shiki-dir', -1.0) # 这里的 key 需要确认是否为探索界面的确认
        blue_exit = self.ctx.pos_obj.get('common-blue-exit',-1.0)
        if sd_id in res and blue_exit in res:
            self.k28_count += 1
            if self.k28_count >= 6:
                print("\n>>> 已位于k28，切换状态")
                tmp = StateK28Zone(self.ctx)
                tmp.ctx.init_k28_count() # 进入k28场景时重置计数
                return tmp #StateK28Zone(self.ctx)
        # [场景B] 可能是点击失效了，还在探索界面，切回探索状态
        k28_box_small = self.ctx.pos_obj.get('k28-box-small', -1.0)
        realm_logo = self.ctx.pos_obj.get('realm-logo', -1.0)
        if k28_box_small in res and realm_logo in res:
            self.tansuo_count += 1
            if self.tansuo_count >= 6:
                print(">>> 切回探索状态")
                return StateExploration(self.ctx)
        # [场景C] 检测突破门票，9的倍数则前往突破
        realm_ticket = self.ctx.pos_obj.get('realm-ticket', -1.0)
        if realm_ticket in res:
            if self.ctx.situation == 0:    
                result, tupo_ticket = get_tickets(self.ctx.current_image)
                if result and tupo_ticket >= 9:
                    print(">>> 突破门票达标，准备进入突破")
                    # 设置标记位，开始返回探索前往突破
                    self.ctx.situation = 1
                    self.ctx.realm_tickets = tupo_ticket
            else:
                common_red_exit = self.ctx.pos_obj.get('common-red-exit', -1.0)
                if common_red_exit in res:
                    print(">>> 返回探索...")
                    target = self.find_best_click_pos(res[common_red_exit], rule='right')
                    self.click_xy(target)
                    sleep(0.5) # 等待动画
        # [场景D] 检测 'k28-box-big' 大盒子，点击确认按钮进入
        k28_box_big = self.ctx.pos_obj.get('k28-box-big', -1.0)
        confirm_id = self.ctx.pos_obj.get('common-yellow-confirm', -1.0)
        if k28_box_big in res and confirm_id in res:
            print(">>> 发现确认按钮，点击进入k28场景")
            target = self.find_best_click_pos(res[confirm_id], rule='right')
            self.click_xy(target)
            sleep(0.5) # 等待动画
        
        # 如果啥都没找到，继续等
        return self

    def on_exit(self):
        pass


# --- 状态：K28 场景内 ---
class StateK28Zone(BaseState):
    def on_enter(self):
        print(">>> [状态] K28 场景内 - 智能索敌ing")
        self.detect_num = 0
        self.tansuo_count = 0
        self.k28Box_count = 0
        self.confirm_count = 0

    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen():
            print(">>> 画面获取失败，继续等待...")
            return self # 画面获取失败，下一帧再试

        # 2. 识别 (使用 k28 模型)
        res, _ = self.detect(self.ctx.model_k28, conf=0.3, imgsz=320)
        res_gen, _ = self.detect(self.ctx.model_general, conf=0.3)

        # 3. 决策逻辑
        flame_id = self.ctx.pos_obj.get('flame', -1.0) # 可能的目标标志
        # [场景A] 可能已经位于战斗界面
        attack_exit = self.ctx.pos_obj.get('attack-exit', -1.0) # 战斗中途退出的按钮
        auto_logo = self.ctx.pos_obj.get('auto-logo', -1.0) # 战斗中自动战斗的标志
        if (attack_exit in res_gen and auto_logo in res_gen):# or flame_id in res_gen:
            print(">>> 尝试进入战斗状态")
            return StateCombat(self.ctx)
        # [场景B] 实际位于k28Box界面
        k28_box_big = self.ctx.pos_obj.get('k28-box-big', -1.0)
        common_red_exit = self.ctx.pos_obj.get('common-red-exit', -1.0)
        if k28_box_big in res_gen and common_red_exit in res_gen:
            self.k28Box_count += 1
            if self.k28Box_count >= 3:
                print(">>> k28可能回到了k28入口界面")
                return StateK28Box(self.ctx)
        # [场景C] 可能回到了探索界面
        exit_id = self.ctx.pos_obj.get('common-blue-exit', -1.0)
        realm_logo = self.ctx.pos_obj.get('realm-logo',-1.0)
        if exit_id in res_gen and realm_logo in res_gen:
            self.tansuo_count += 1
            if self.tansuo_count >= 3:
                print(">>> k28可能回到了探索界面")
                return StateExploration(self.ctx)
        # [场景D] 掉落宝箱，点击领取
        k28_success_box = self.ctx.pos_obj.get('k28-success-box', -1.0)
        if k28_success_box in res_gen:
            print(">>> 发现掉落宝箱，点击领取")
            target = self.find_best_click_pos(res_gen[k28_success_box])
            self.click_xy(target)
            sleep(0.3)
            return StateCombat(self.ctx)
        # [场景E] 检测 达摩/经验加成 目标，点击战斗图标进入战斗
        combat_id = self.ctx.k28_obj.get('tansuo_combat', -1.0)
        damo_id = self.ctx.k28_obj.get('tansuo_damo', -1.0)
        gold_id = self.ctx.k28_obj.get('tansuo_jinbi', -1.0)
        ## 提取框列表 (如果没有则为空列表)
        combat_boxes = res.get(combat_id, [])
        gold_boxes    = res.get(gold_id, [])
        damo_boxes   = res.get(damo_id, [])
        if combat_boxes:
            if damo_boxes:
                target = self.select_optimal_monster(combat_boxes, gold_boxes, damo_boxes)
                if target:
                    print(f">>> 锁定目标 (优先级策略), 点击进攻")
                    self.click_xy(target)
                    sleep(0.2) # 等待动画
                    return self #StateCombat(self.ctx)
                else:
                    print(">>> 未能选出合适目标，继续搜索...")
        else:
            if self.ctx.move_count >= 6 and self.ctx.k28_exit_flag == 0:
                sleep(0.6)
                self.ctx.k28_exit_flag = 1
                return self
        # [场景F] 存在退出确认框，点击返回k28Box
        confirm_id = self.ctx.pos_obj.get('common-yellow-confirm', -1.0)
        common_red_exit = self.ctx.pos_obj.get('common-red-exit', -1.0)
        realm_ticket = self.ctx.pos_obj.get('realm-ticket', -1.0)
        if confirm_id in res_gen and common_red_exit not in res_gen and realm_ticket not in res_gen:
            self.confirm_count += 1
            if self.confirm_count >= 3:
                print(">>> 发现退出确认框，点击返回k28入口")
                target = self.find_best_click_pos(res_gen[confirm_id], rule='right')
                self.click_xy(target)
                sleep(0.6) # 等待动画
                # return StateK28Box(self.ctx)
                #return self
        # [场景G] 未通关，无宝箱，可能需要移动视角或滑动屏幕，一直未发现目标则退出
        if self.detect_num >= 18:
            self.detect_num = 0
            if self.ctx.move_count < 6:
                print(">>> 未发现目标，尝试滑动屏幕寻找...")
                self.perform_move()
            else:
                if exit_id in res_gen:
                    print(">>> 没有高收益目标，点击传送门退出")
                    target = self.find_best_click_pos(res_gen[exit_id])
                    self.click_xy(target)
                    sleep(0.1) # 等待动画
                else:
                    print(">>> 未发现退出按钮，存在问题...")
        else:
            self.detect_num += 1
        
        # 如果啥都没找到，继续等
        return self
    

    def on_exit(self):
        pass

    def select_optimal_monster(self, combat_boxes, gold_boxes, damo_boxes):
        """
        优先级选择算法：
        1. 达摩怪 (Damo)
        2. 金币怪 (Gold)
        3. 普通怪 (Normal) - 优先选最右边的(通常是新刷出来的)
        """
        # # 如果没有 Buff 框，直接返回最右边的怪
        # if not gold_boxes and not damo_boxes:
        #     # 策略：rule='right'，打最右边的怪，方便一路往右清
        #     return self.find_best_click_pos(combat_boxes, rule='right')

        best_target = None
        best_score = 0
        for m_box in combat_boxes:
            # m_box: [x1, y1, x2, y2]
            # 计算怪物中心点
            mx = (m_box[0] + m_box[2]) / 2
            my = (m_box[1] + m_box[3]) / 2
            score = 0 # 基础分
            # --- 匹配达摩 Buff ---
            # 判定标准：Buff 在怪物的“下方”且“动态环绕”
            # x 轴容差：怪物宽度的 80%
            # y 轴判定：Buff y2 应该小于 怪物 y1 (即在怪物上方)
            width = m_box[2] - m_box[0]
            # 检查是否携带 Damo
            for d_box in damo_boxes:
                dx = (d_box[0] + d_box[2]) / 2
                dy = (d_box[1] + d_box[3]) / 2
                dy1 = d_box[1] ; dy2 = d_box[3]
                # 水平偏差 < 0.1 (归一化坐标) 且 Buff在怪物上方
                if abs(dx - mx) < 0.11 and abs(dy - my) < 0.4 and abs(dy - my) > 0.06:
                    score = 200 # damo怪加 200 分
                    break # 一个怪只能有一个同类 buff
            
            # 检查是否携带 Gold (如果没加过分)
            if score == 0:
                for g_box in damo_boxes:
                    gx = (g_box[0] + g_box[2]) / 2
                    gy1 = g_box[1] ; gy2 = g_box[3]
                    # 水平偏差 < 0.08 且 Buff在怪物上方
                    if abs(gx - mx) < 0.08 and (my+0.2) > gy1 and (my + 0.2) < gy2:
                        score = 100 # 金币怪加 50 分
                        break
            
            # 如果分数 > 0，说明是有 Buff 的怪
            # 距离加分：稍微优先打左边的，防止打完怪回头找的时候漏掉
            # x 坐标越大 (越靠右)，加 0~1 分
            # score += mx 
            if score > 0 and score > best_score:
                best_score = score
                best_target = m_box
            
        #     scored_monsters.append((score, m_box))

        # # 按分数降序排列
        # scored_monsters.sort(key=lambda x: x[0], reverse=True)
        # best_score, best_box = scored_monsters[0]
        # type_str = "普通"
        # if best_score >= 100: type_str = "经验"
        # elif best_score >= 50: type_str = "金币"
        # print(f" -> 选敌结果: {type_str}怪 (分值:{best_score:.2f})")
        return best_target

    def perform_move(self):
        """执行移动/滑动逻辑"""
        self.ctx.move_count += 1
        # 每几次尝试点一下右边，模拟移动
        # 注意：这里最好实现真正的 Drag/Swipe，或者点击边缘
        self.click_xy([0.90,0.66,0.95,0.72])
        sleep(0.01) # 等待画面更新
        

# --- 状态：战斗中 ---
class StateCombat(BaseState):
    def on_enter(self):
        print("\n>>> [状态] 战斗判定中...")
        self.start_time = time.time()
        self.check_interval = 0
        self.success_detected_num = 0
        self.failure_detected_num = 0
        self.k28_detected_num = 0

    def execute(self):
        # 超时保护 (3分钟没动静)
        if time.time() - self.start_time > 180:
            print(">>> [警告] 战斗超时")
            return StateExploration(self.ctx) # 强行切回探索尝试恢复
        # 降频检测，k28战斗不需要每帧都看，省CPU
        self.check_interval += 1
        if self.ctx.situation == 0 and self.check_interval < 30:
            sleep(0.1)
            return self

        # 1. 刷新画面
        if not self.ctx.update_screen(): return self

        # 2. 识别 (使用 general 模型)
        res, _ = self.detect(self.ctx.model_general, conf=0.3)
        
        # [场景A] 战斗胜利 (达摩或箱子)
        success_damo = self.ctx.pos_obj.get('success-damo', -1.0)
        k28_success_box = self.ctx.pos_obj.get('k28-success-box', -1.0) # 结算箱子
        if success_damo in res or k28_success_box in res:
            self.success_detected_num += 1
            # 连续确认3次才算真赢了，防止误判
            if self.success_detected_num >= 3:
                print(">>> 收菜结算")
                return StateSettlement(self.ctx)
        # [场景B] 战斗失败
        failed_logo = self.ctx.pos_obj.get('failed-logo', -1.0)
        if failed_logo in res:
            print(">>> 战斗失败")
            # self.failure_detected_num += 1
            # if self.failure_detected_num >= 3:
            return StateSettlement(self.ctx)

        attack_exit = self.ctx.pos_obj.get('attack-exit', -1.0) # 战斗中途退出的按钮
        # [场景C] 本轮突破仅剩最后一个目标，需要投降4次避免对手升级
        if self.ctx.situation == 1 and self.ctx.realm_target_num == 1:
            common_red_cancel = self.ctx.pos_obj.get('common-red-cancel', -1.0) # 投降确认框的取消按钮
            if common_red_cancel in res:
                print(">>> 突破仅剩最后一个目标，点击投降...")
                target = self.find_best_click_pos(res[common_red_cancel], rule='right')
                self.click_xy(target) # 点击投降按钮
                sleep(0.1) # 等待动画
            elif attack_exit in res:
                print(">>> 突破仅剩最后一个目标，投降一次...")
                target = self.find_best_click_pos(res[attack_exit])
                self.click_xy(target) # 点击退出按钮
                sleep(0.1) # 等待动画
        # [场景D] 战斗中 or 并未发生战斗
        auto_logo = self.ctx.pos_obj.get('auto-logo', -1.0) # 战斗中自动战斗的标志
        buff_logo = self.ctx.pos_obj.get('buff-logo', -1.0) # 结算界面的buff标志
        common_blue_exit = self.ctx.pos_obj.get('common-blue-exit', -1.0) # 结算界面的退出按钮
        if attack_exit in res and auto_logo in res:
            print(">>> 战斗中")
        elif common_blue_exit in res and buff_logo in res:
            self.k28_detected_num += 1
            if self.k28_detected_num >= 3:
                print(">>> 可能并未发生战斗，切换回",end="")
                if self.ctx.situation == 1:
                    print("突破界面")
                    return StateTupoList(self.ctx)
                else:
                    print("k28界面")
                    return StateK28Zone(self.ctx)
            


        return self

    def on_exit(self):
        pass

# --- 状态：结算 ---
class StateSettlement(BaseState):
    def on_enter(self):
        print(">>> [状态] 结算界面")
        self.click_count = 0
        self.pre_click_time = 0
        self.small_num = 0
        self.big_num = 0
        self.k28_num = 0
        self.realm_count = 0

    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen(): return self
        
        # 2. 识别 (使用两个模型一起)
        res, _ = self.detect(self.ctx.model_general, conf=0.3)
        # res_k28, _ = self.detect(self.ctx.model_k28, conf=0.3, imgsz=320)
        
        # 3. 决策逻辑
        # 进入结算状态默认点击一次边缘或是检测胜利达摩
        success_damo = self.ctx.pos_obj.get("success-damo",-1.0)
        if success_damo in res:
            # self.click_xy( [0.8, 0.8, 0.9, 0.9])
            self.click_xy([0.90,0.66,0.95,0.72])
            sleep(0.3) 
        # 简单粗暴的结算逻辑：有东西就点，没东西点空白，直到看到探索界面
        elif time.time() - self.pre_click_time > 0.15:
            self.click_xy([0.90,0.66,0.95,0.72])
            self.pre_click_time = time.time()
            self.click_count += 1

        # [场景A] 已经回到k28场景
        buff_logo = self.ctx.pos_obj.get('buff-logo', -1.0)
        tansuo_combat = self.ctx.k28_obj.get('tansuo_combat', -1.0)
        common_blue_exit = self.ctx.pos_obj.get('common-blue-exit', -1.0)
        shaki_dir = self.ctx.pos_obj.get('shiki-dir', -1.0)
        if common_blue_exit in res and buff_logo in res:
            self.k28_num += 1
            if self.k28_num == 3:
                print(">>> 战斗结算完成，回到上一场景")
                #self.ctx.loop_count += 1
                return StateK28Zone(self.ctx)
        
        # [场景B] 识别到k28-box-big，说明回到了k28入口界面
        k28_box_big = self.ctx.pos_obj.get('k28-box-big', -1.0)
        if k28_box_big in res:
            self.big_num += 1
            if self.big_num == 3:
                print(">>> 回到K28入口界面")
                return StateK28Box(self.ctx)

        # [场景C] 识别到k28-box-small，说明回到了探索界面
        k28_box_small = self.ctx.pos_obj.get('k28-box-small', -1.0)
        if k28_box_small in res:
            self.small_num += 1
            if self.small_num == 3:
                print(">>> 回到探索界面")
                self.ctx.loop_count += 1
                return StateExploration(self.ctx)
        
        # [场景D] 识别到突破界面，返回突破
        realm_wait = self.ctx.pos_obj.get('realm-wait', -1.0) # 突破目标-等待挑战
        realm_again = self.ctx.pos_obj.get('realm-again', -1.0) # 突破目标-再次挑战
        realm_success = self.ctx.pos_obj.get('realm-success', -1.0) # 突破目标-成功
        if realm_wait in res or realm_again in res or realm_success in res:
            self.realm_count += 1
            if self.realm_count == 3:
                print(">>> 可能回到了突破界面，切换状态")
                return StateTupoList(self.ctx)

        
        # 防死循环
        if self.click_count > 30:
             return StateExploration(self.ctx)

        return self

    def on_exit(self):
        pass

# ==============================================================================
# 4. 状态机引擎 (Engine) - 驱动程序
# ==============================================================================
class GameEngine:
    def __init__(self):
        self.ctx = GameContext()
        # 初始状态设为探索
        self.current_state = StateExploration(self.ctx)
        #self.current_state.on_enter()
        
    def start(self):
        print("========== 阴阳师自动化引擎启动 (按 Ctrl+C 安全退出) ==========")
        
        self.current_state.on_enter()
        
        try:
            while self.ctx.running:
                # 1. 执行当前状态逻辑
                next_state = self.current_state.execute()
                
                # 2. 状态切换
                if next_state and next_state != self.current_state:
                    self.current_state.on_exit()
                    self.current_state = next_state
                    self.current_state.on_enter()
                
                # 3. 只有当没有进行任何耗时操作时，才sleep，防止CPU占用过高
                # 但execute内部通常包含了识别和点击，所以这里给一个微小的sleep即可
                sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n>>> 用户停止")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"\n>>> [严重错误] {e}")
        finally:
            self.shutdown()

    def shutdown(self):
        print(">>> 正在释放资源...")
        self.ctx.running = False
        release_capture() # 释放DLL资源
        print(">>> 资源已释放，进程即将结束。")

# 调试用入口
if __name__ == "__main__":
    # 需要先手动初始化 yys_config 中的窗口句柄，实际使用时由 yys_main.py 调用
    # 这里仅做类结构检查，直接运行会因为句柄为0无效
    print("请通过 yys_main.py 调用或在此处添加句柄初始化代码")
    pass