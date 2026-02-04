# -*- coding: utf-8 -*-
import time
from abc import ABC, abstractmethod
from ultralytics import YOLOv10

# 引入原有项目依赖
import yys_config
from yys_util import get_windows, mouse_click, sleep
from yys_windows import release_capture

# ==============================================================================
# 1. 上下文管理器 (Context) - 核心资源与数据总线
# ==============================================================================
class GameContext:
    def __init__(self):
        self.running = True
        self.model_k28 = None
        self.model_tupo = None
        
        # 运行时数据
        self.current_image = None
        self.yolo_results = None  # 缓存最近一次识别结果
        
        # 统计数据
        self.loop_count = 0       # 刷本次数
        self.target_count = 0     # 目标次数 (从配置读或输入)
        
        # 加载配置中的坐标映射 (直接引用 yys_config 中的定义)
        self.pos_obj = yys_config.pos_obj
        self.k28_obj = yys_config.k28_obj

        # 初始化模型
        self._init_models()

    def _init_models(self):
        print(">>> [FSM] 正在加载 AI 模型...")
        try:
            self.model_k28 = YOLOv10("./models/k28.pt")
            self.model_tupo = YOLOv10('./models/last.pt') # 假设 last.pt 是通用检测
            print(">>> [FSM] 模型加载完成")
        except Exception as e:
            print(f">>> [错误] 模型加载失败: {e}")
            self.running = False

    def update_screen(self, timeout=10.0):
        """
        核心修复：阻塞式获取画面，防止 YOLO 接收 None 报错
        """
        start_time = time.time()
        while True:
            # 尝试获取画面
            img = get_windows()
            
            if img is not None:
                self.current_image = img
                return True
            
            # 超时检测
            if time.time() - start_time > timeout:
                print(f"\n[警告] 无法获取游戏画面 (已重试 {timeout}s)，请检查窗口是否被遮挡")
                return False
            
            # 避免死锁和 CPU 空转
            time.sleep(0.02)

# ==============================================================================
# 2. 状态基类 (Base State)
# ==============================================================================
class BaseState(ABC):
    def __init__(self, ctx: GameContext):
        self.ctx = ctx
        self.pos_obj = ctx.pos_obj # 快捷引用

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

    # --- 通用工具方法 ---
    def detect(self, model, conf=0.25):
        """执行 YOLO 识别并返回去重后的 key 列表"""
        if not self.ctx.current_image:
            return {}, []
        
        try:
            # 1. 推理
            results = model(self.ctx.current_image, imgsz=640, conf=conf, verbose=False)
            
            # 2. 简易解析 (这里暂简化了原有的 self_dedup 逻辑，优先跑通流程)
            # 返回格式： {class_id: [[x1, y1, x2, y2], ...]}
            detected_dict = {} 
            raw_results = results[0]
            
            if raw_results.boxes:
                for box in raw_results.boxes:
                    cls_id = float(box.cls)
                    xyxyn = box.xyxyn.tolist()[0] # 归一化坐标
                    
                    if cls_id not in detected_dict:
                        detected_dict[cls_id] = []
                    detected_dict[cls_id].append(xyxyn)
                    
            return detected_dict, raw_results
        except Exception as e:
            print(f"[识别错误] {e}")
            return {}, []

    def find_best_click_pos(self, box_list):
        """从多个框中找到最适合点击的一个 (默认取第一个，可扩展逻辑)"""
        if not box_list:
            return None
        # 简单策略：取第一个
        return box_list[0]

# ==============================================================================
# 3. 具体业务状态实现 (以 K28 流程为例)
# ==============================================================================

# --- 状态：探索/找怪 (对应原来的 k28 逻辑) ---
class StateExploration(BaseState):
    def on_enter(self):
        print(f"\r>>> [状态] 探索中... (已完成: {self.ctx.loop_count})", end="")

    def execute(self):
        # 1. 刷新画面
        if not self.ctx.update_screen():
            return self # 画面获取失败，下一帧再试

        # 2. 识别 (使用 K28 模型)
        # 注意：这里需要确保 model_k28 能识别原来的 'tansuo_combat' 等
        obj_map, _ = self.detect(self.ctx.model_k28, conf=0.25)
        
        # 3. 决策逻辑
        k28_combat_id = self.ctx.k28_obj.get('tansuo_combat', -1.0)
        k28_box_small = self.ctx.pos_obj.get('k28-box-small', -1.0) # 纸人小盒子
        
        # [场景A] 发现怪物 -> 点击 -> 进战斗
        if k28_combat_id in obj_map:
            print("\n>>> 发现怪物，发起进攻")
            target = self.find_best_click_pos(obj_map[k28_combat_id])
            mouse_click(yys_config.yys_click_window, target)
            return StateCombat(self.ctx)

        # [场景B] 发现战利品盒子 -> 点击 -> 领奖
        if k28_box_small in obj_map:
            print("\n>>> 发现战利品，领取中")
            target = self.find_best_click_pos(obj_map[k28_box_small])
            mouse_click(yys_config.yys_click_window, target)
            sleep(1.0) # 等待动画
            return self # 领完继续找

        # [场景C] 误入战斗准备界面 (有时候点怪没点好)
        ready_id = self.ctx.pos_obj.get('ready', -1.0)
        if ready_id in obj_map:
             return StateCombat(self.ctx)

        # [场景D] 啥都没找到 -> 防卡死/随机点击右边空白处移动
        # print(" 未发现目标", end="")
        # 可以在这里加一个滑动或者点击空白的逻辑
        # click_xy([0.90, 0.66, 0.95, 0.72]) # 原有代码中的防卡死点击
        
        return self

    def on_exit(self):
        pass

# --- 状态：战斗中 ---
class StateCombat(BaseState):
    def on_enter(self):
        print("\n>>> [状态] 战斗进行中...")
        self.start_time = time.time()
        self.check_interval = 0

    def execute(self):
        # 降频检测，战斗不需要每帧都看，省CPU
        self.check_interval += 1
        if self.check_interval < 5: 
            sleep(0.1)
            return self
        self.check_interval = 0

        if not self.ctx.update_screen(): return self

        # 识别 (使用通用/Tupo模型来识别胜利失败)
        obj_map, _ = self.detect(self.ctx.model_tupo, conf=0.20)
        
        success_damo = self.ctx.pos_obj.get('success-damo', -1.0)
        failed_logo = self.ctx.pos_obj.get('failed-logo', -1.0)
        k28_success_box = self.ctx.pos_obj.get('k28-success-box', -1.0) # 结算箱子

        # [场景A] 战斗胜利 (达摩或箱子)
        if success_damo in obj_map or k28_success_box in obj_map:
            print(">>> 战斗胜利")
            return StateSettlement(self.ctx)

        # [场景B] 战斗失败
        if failed_logo in obj_map:
            print(">>> 战斗失败")
            return StateSettlement(self.ctx)

        # 超时保护 (5分钟没动静)
        if time.time() - self.start_time > 300:
            print(">>> [警告] 战斗超时")
            return StateExploration(self.ctx) # 强行切回探索尝试恢复

        return self

    def on_exit(self):
        pass

# --- 状态：结算 ---
class StateSettlement(BaseState):
    def on_enter(self):
        print(">>> [状态] 结算界面")
        self.click_count = 0

    def execute(self):
        if not self.ctx.update_screen(): return self
        
        # 简单粗暴的结算逻辑：有东西就点，没东西点空白，直到看到探索界面
        
        # 1. 检查是否已经回到了探索界面 (通过检测 buff图标 或 探索UI特征)
        # 这里为了简化，假设检测到 buff-logo 或者 exploration UI 就退
        obj_map_k28, _ = self.detect(self.ctx.model_k28, conf=0.25)
        
        # 原有代码逻辑：检测到 'tansuo_combat' 或者 'buff-logo' 说明出来了
        # 假设 buff-logo 在 pos_obj 里
        buff_logo = self.ctx.pos_obj.get('buff-logo', -1.0)
        
        if buff_logo in obj_map_k28:
            print(">>> 结算完成，返回探索")
            self.ctx.loop_count += 1
            return StateExploration(self.ctx)

        # 2. 还在结算，点击屏幕右下角/空白处跳过动画
        # 模拟点击 [0.0065,0.61635,0.0295,0.6395] 或者是原有代码的习惯位置
        # 这里使用一个通用的空白位置
        mouse_click(yys_config.yys_click_window, [0.8, 0.8, 0.9, 0.9])
        sleep(0.5) 
        self.click_count += 1
        
        # 防死循环
        if self.click_count > 20:
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