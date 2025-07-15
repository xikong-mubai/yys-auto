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



# print('hello')

# from yys_util import check_windows

# check_windows("test")
import ctypes,os,time
import numpy as np

# 添加 DLL 目录到 PATH
DLL_PATH = "E:\\study\\code\\c++\\windows-identify\\x64\\Release\\windows-capture\\windows-capture.dll"
os.environ["PATH"] = os.path.dirname(DLL_PATH) + ";" + os.environ["PATH"]
# 加载 DLL
#capture = ctypes.WinDLL(DLL_PATH)

# "E:\study\code\c++\windows-identify\x64\Debug\windows-capture\windows-capture.dll"
#dll = ctypes.cdll.LoadLibrary("..\\..\\c++\\windows-identify\\x64\\Debug\\windows-capture\\windows-capture.dll")
#dll = ctypes.WinDLL("E:\\study\\code\\c++\\windows-identify\\x64\\Release\\windows-capture\\windows-capture.dll")
dll = ctypes.cdll.LoadLibrary("E:\\study\\code\\c++\\windows-identify\\x64\\Release\\windows-capture\\windows-capture.dll")
#dll = ctypes.WinDLL(" E:\\study\\code\\c++\\windows-identify\\x64\\Debug\\windows-capture\\windows-capture.dll")

init_capture = dll.init_capture
update_frame= dll.update_frame
get_frame = dll.get_frame
stop_capture = dll.stop_capture

init_capture.argtypes = [ctypes.c_void_p]
get_frame.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int,
                      ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
get_frame.restype = ctypes.c_bool
update_frame.restype = ctypes.c_bool

# from yys_main import get_window_handle
# import win32gui
# hwnd_1 = win32gui.FindWindow(None, "MuMu多开器12")
# print(hwnd_1)
# windows = get_window_handle()
# print(windows)
# exit()
# hwnd = ctypes.c_void_p(windows[0][0])
# hwnd = ctypes.c_void_p(397678)
hwnd = ctypes.c_void_p(3544594)
# hwnd_p = ctypes.c_void_p(hwnd)
# exit()
# print(hwnd)
# 传入目标 HWND
init_capture(hwnd)

# 接收帧数据
buffer = (ctypes.c_uint8 * (1920*1080*3))()
BUFFER_SIZE = 1920*1080*3
width = ctypes.c_int()
height = ctypes.c_int()
print("就这？")
time.sleep(1)

from PIL import Image, ImageTk
import tkinter as tk
import threading
frame_ready = threading.Event()
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

        if get_frame(buffer, BUFFER_SIZE, ctypes.byref(width), ctypes.byref(height)):
            try:
                img_array = np.ctypeslib.as_array(buffer, shape=(width.value * height.value * 3,))
                img_array = img_array[:width.value * height.value * 3]  # 截取有效数据
                img_array = img_array.reshape((height.value, width.value, 3))
                img = Image.fromarray(img_array, 'RGB')
                img_tk = ImageTk.PhotoImage(image=img)

                canvas.config(image=img_tk)
                canvas.image = img_tk
            except Exception as e:
                print("Image decode error:", e)

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


# 定义回调类型：__stdcall(void)
CALLBACK_TYPE = ctypes.WINFUNCTYPE(None)

# 定义 Python 回调函数
@CALLBACK_TYPE
def on_new_frame():
    print("New frame arrived!")
    frame_ready.set()
    # 可以在这里设置事件或触发 UI 刷新

# 注册回调函数到 DLL
dll.register_frame_callback(on_new_frame)

# 启动画面更新
update_tk_frame()

# 程序关闭时释放资源
def on_close():
    dll.stop_capture()
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




stop_capture()




