from PIL import Image, ImageTk, ImageDraw,ImageFont
import colorsys

def draw_annotation(img, annot:dict):
    """
    batch=True时表示批量处理图像，False表示绘制单张图像并且显示
    img_path: 如果batch=True，则为图像集的dir_path；否则表示单张图像的path
    annot_path： 标注`txt`文件的路径
    save_path：当batch=True才有效，表示绘制框后的图像保存的dir_path
    classes_path: `class`文件的path
    """
    class_names = ['again-attack', 'attack-exit', 'auto-logo', 'buff-logo', 'common-blue-exit', 'common-box-confirm', 'common-red-cancel', 'common-red-exit', 'common-yellow-confirm', 'e-mail', 'failed-logo', 'flame', 'goxie-accept', 'goxie-logo', 'goxie-refuse', 'huijuan-big', 'huijuan-normal', 'huijuan-small', 'k28-box-big', 'k28-box-small', 'k28-success-box', 'ready', 'realm-again', 'realm-logo', 'realm-success', 'realm-ticket', 'realm-wait', 'royal-logo', 'shiki-dir', 'soul-logo', 'success-damo', 'willpower', 'world-message']
    #class_names = ['tansuo_combat', 'tansuo_damo', 'tansuo_jinbi', 'tansuo_jingyan']
    num_classes = len(class_names)
    
    print(annot)
    # 设置不同类别的框的颜色（r,g,b）
    hsv_tuples = [(x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))

    image = img
    weight,height = image.size

    font = ImageFont.truetype(font='model_data/simhei.ttf',
                                size=np.floor(3e-2 * height + 0.5).astype('int32'))
    thickness = int(
        max((weight + height) // np.mean(np.array(image.size[:2])), 1))

    # time.sleep(5)
    # print(annot)
    draw = ImageDraw.Draw(image)
    for line in annot.keys():
        for box in annot[line]:
            left, top, right, bottom = box
            cls_id = line
            top     = max(0, int(top*height))
            left    = max(0, int(left*weight))
            bottom  = min(height, int(bottom*height))
            right   = min(weight, int(right*weight))
            
            label = '{}'.format(class_names[int(cls_id)])

            label_size = draw.textbbox(xy=(left,top),text=label,font=font)
            label_size = (label_size[2]-label_size[0],label_size[3]-label_size[1])
            label = label.encode('utf-8')
            print(label, top, left, bottom, right)

            # if bottom - top - label_size[1] >= 0:
            #     text_origin = np.array([left, top - label_size[1]])
            # else:
            #     text_origin = np.array([left, top + 1])
            text_origin = np.array([left, top - label_size[1]])
            for i in range(thickness):
                draw.rectangle([left + i, top + i, right - i, bottom - i], outline=colors[int(cls_id)])
            draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=colors[int(cls_id)])
            draw.text(text_origin, str(label,'UTF-8'), fill=(0,0,0), font=font)

    del draw
            
    return image



# from os import path
# import os

# # with open('pure','r') as f:
# #     for  i in f.readlines():
# #         name,src,type = i.strip().split('  ')
# #         name = name.replace('.', os.sep)
# #         init = path.join(name, '__init__.py')
# #         pos = src.find(init) if init in src else src.find(name)

# #         dst = src[pos:]
# #         dst = path.join('libs', dst)
# #         if pos == -1:
# #             print(name,dst,src)

            
#         # if dst.count('\\') == 1:
#         #     print(dst, src, 'DATA')  # 不需要打包的第三方依赖 py 文件引到 libs 文件夹
# a = '''
# 1111111001000101111111111
# 1000001001110010000001001
# 1011110101010110110101011
# 1011110101001001000001111
# 1011110101000100110101111
# 1000001000000000000001001
# 1111111001001010101111111
# 0000000000001100000000000
# 1110111111111110001100001
# 1011000001111010111100011
# 0001111011111111111111111
# 1000000000000100000000000
# 1110111100000011000000000
# 0000000000001010111111100
# 1111111010111100000011100
# 1011110101001011101010110
# 1011110101010101111011111
# 1011100101001110111111100
# 1111111001010101111100010
# 1000001000000000010000010
# 1111111111111000111111111'''
# # a = (a.split('\n'))
# a = a.replace('\n','')
# print(len(a))
# # from PIL import Image
# # img = Image.new('1',(25,21))
# # for i in range(21):
# #     for j in range(25):
# #         if a[i][j] == '1':
# #             img.putpixel((j,i),0)
# #         else:
# #             img.putpixel((j,i),1)

# # img.show()
# # img.save('F:\\temp\\Downloads\\tmp.png')
# # img.close()
from ultralytics import YOLOv10
global model_k28,model_tupo
print("初始化AI模型...")
try:
    model_k28 = YOLOv10("./models/k28.pt")
    model_tupo = YOLOv10('./models/best.pt')
    print("初始化成功")
except Exception as e:
    print("模型加载出现问题：",e)
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
    try:
        result = model_k28(image,imgsz=320,conf=0.3)
    except Exception as e:
        print("模型识别遇到问题",e)
        return False,e,None
    for r in result:
        r = self_dedup(r)
        real_r = r.keys()
        if len(real_r) != 0:
            return True,"enemies exist",r
    return False,"no things",None

def no_k28_check(image):
    try:
        result = model_tupo(image,imgsz=640,conf=0.3)
    except Exception as e:
        print("模型识别遇到问题",e)
        return False,e,None
    for r in result:
        r = self_dedup(r)
        real_r = r.keys()
        if len(real_r) != 0:
            return True,"objections exist",r
    return False,"no things",None

import ctypes,os,time,threading
import numpy as np
from multiprocessing import freeze_support
freeze_support()
# 添加 DLL 目录到 PATH
DLL_PATH = "./windows-capture.dll"
# os.environ["PATH"] = os.path.dirname(DLL_PATH) + ";" + os.environ["PATH"]
# 加载 DLL
#capture = ctypes.WinDLL(DLL_PATH)
# "E:\study\code\c++\windows-identify\x64\Debug\windows-capture\windows-capture.dll"
#dll = ctypes.cdll.LoadLibrary("..\\..\\c++\\windows-identify\\x64\\Debug\\windows-capture\\windows-capture.dll")
#dll = ctypes.WinDLL("E:\\study\\code\\c++\\windows-identify\\x64\\Release\\windows-capture\\windows-capture.dll")
test_dll = ctypes.cdll.LoadLibrary(DLL_PATH)
#dll = ctypes.WinDLL(" E:\\study\\code\\c++\\windows-identify\\x64\\Debug\\windows-capture\\windows-capture.dll")

init_capture = test_dll.init_capture
#update_frame= dll.update_frame
get_frame = test_dll.get_frame
stop_capture = test_dll.stop_capture

init_capture.argtypes = [ctypes.c_void_p]
get_frame.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int,
                      ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
                      ctypes.POINTER(ctypes.c_uint64)]
get_frame.restype = ctypes.c_bool
#update_frame.restype = ctypes.c_bool

frame_ready = threading.Event()
# 定义回调类型：__stdcall(void)
CALLBACK_TYPE = ctypes.WINFUNCTYPE(None)
# 定义 Python 回调函数
@CALLBACK_TYPE
def on_new_frame():
    # print("New frame arrived!")
    frame_ready.set()
    # 可以在这里设置事件或触发 UI 刷新
# 注册回调函数到 DLL
test_dll.register_frame_callback(on_new_frame)
time.sleep(1)

import win32gui
def _callback( hwnd, extra ):
    windows = extra
    temp=[]
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #if left == 0 and top == 0 and right < 1280 and right > 640:
    temp.append(hwnd)
    temp.append(win32gui.GetClassName(hwnd))
    temp.append(win32gui.GetWindowText(hwnd))
    temp.append((left, top, right, bottom))
    if len(temp[2]) > 0 and temp[3][2]-temp[3][0] > 6 and temp[3][3] - temp[3][1] > 6 \
        and win32gui.IsWindowVisible(temp[0]):
        windows[hwnd] = temp
def check_windows():
    windows = {} ; length = 0
    dst = []
    win32gui.EnumWindows(_callback, windows)
    # print("Enumerated a total of  windows with %d classes"%(len(windows)))
    for item in windows:
        # if window_name == windows[item][2] and window_name != "":
        dst.append(windows[item])
        length += 1
    if length == 0:
        print("Not found any window what have title.")
        return False,dst
    return True,dst
result,windows = check_windows()
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
    hwnd = ctypes.c_void_p(windows[choose][0])
    init_capture(hwnd)
choose_windows(windows)
# 接收帧数据
buffer = (ctypes.c_uint8 * (1920*1080*3))()
BUFFER_SIZE = 1920*1080*3
width = ctypes.c_int()
height = ctypes.c_int()
out_frame_id = ctypes.c_uint64()
print("就这？")
time.sleep(1)

import tkinter as tk
# GUI 主窗口
root = tk.Tk()
root.title("实时窗口画面捕获")
# 创建 Canvas
canvas = tk.Label(root)
canvas.pack()

# 更新画面函数
def update_tk_frame():
    # 检查是否有新帧
    if frame_ready.is_set():
        frame_ready.clear()
        try:
            if get_frame(buffer, BUFFER_SIZE, ctypes.byref(width), ctypes.byref(height), ctypes.byref(out_frame_id)):
                print(width.value,height.value)
                try:
                    img_array = np.ctypeslib.as_array(buffer, shape=(width.value * height.value * 3,))
                    img_array = img_array[:width.value * height.value * 3]  # 截取有效数据
                    img_array = img_array.reshape((height.value, width.value, 3))
                    img = Image.fromarray(img_array, 'RGB')
                    result,message,r = no_k28_check(img) #k28_check(img)
                    if result:
                        draw_img = draw_annotation(img,r)
                    # #draw_img.show()
                        img_tk = ImageTk.PhotoImage(image=draw_img)
                    else:
                        img_tk = ImageTk.PhotoImage(image=img)
                    #time.sleep(1000)
                    canvas.config(image=img_tk)
                    canvas.image = img_tk
                except Exception as e:
                    print("Image decode error:", e)
        except Exception as error:
            print("\r\nget_window error!!!\n",error)
    root.after(10, update_tk_frame)
    # if get_frame(buffer, BUFFER_SIZE, ctypes.byref(width), ctypes.byref(height)):
    #     w, h = width.value, height.value
    #     img_np = np.ctypeslib.as_array(buffer)[:w*h*3].reshape((h, w, 3))
    #     img = Image.fromarray(img_np, 'RGB')
    #     img_tk = ImageTk.PhotoImage(image=img)

    #     canvas.config(image=img_tk)
    #     canvas.image = img_tk
    # else:
    #     print("---------------oh no ------------")
    # root.after(0, update_tk_frame)  # 每 30ms 更新一帧（约 33fps）

# 启动画面更新
update_tk_frame()

# 程序关闭时释放资源
def on_close():
    # dll.stop_capture()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

# if dll.update_frame():
# #     # ok = dll.get_frame(buffer, buffer_size, out_width_ptr, out_height_ptr)
#     ok = dll.get_frame(buffer, len(buffer), ctypes.byref(width), ctypes.byref(height))
# # if get_frame(buffer, len(buffer), ctypes.byref(width), ctypes.byref(height)):
#     img = np.ctypeslib.as_array(buffer[:width.value*height.value*3]).reshape(height.value, width.value, 3)
#     #img = img.reshape((height.value, width.value, 3))
#     print("success get frame:", img.shape)
# else:
#     time.sleep(0.5)  # 无新帧，短暂等待，避免占满 CPU

# stop_capture()
