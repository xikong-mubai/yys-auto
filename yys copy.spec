# -*- mode: python ; coding: utf-8 -*-

from importlib.util import find_spec	# 用于查找模块所在路径
from os.path import dirname
from os import path
from pprint import pprint
import os, re


block_cipher = None
# 空列表，用于准备要复制的数据
datas = []

# 这是要额外复制的模块
manual_modules = ['ultralytics']
for m in manual_modules:
    if not find_spec(m): continue
    p1 = dirname(find_spec(m).origin)
    p2 = m
    datas.append((p1, p2))

# 这是要额外复制的文件夹
my_folders = ['models','img']
for f in my_folders:
    datas.append((f, f))

# 这是要额外复制的文件
my_files = ['version', 'yysauto.json','readme.txt']
for f in my_files:
    datas.append((f, '.'))      # 复制到打包导出的根目录
    
    
# ==================新建 a 变量，分析脚本============================

a = Analysis(
    ['yys.py'],
    pathex=['F:\\study\\code\\python\\yys-ai-cpu\\Lib\\site-packages\\torch\\lib'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook.py'],
    excludes=["IPython"],
    noarchive=False,
    optimize=0,
)

#===================分析完成后，重定向 a 的二进制、py文件到 libs 文件夹================================


# 把 a.datas 中不属于自定义的文件重定向到 libs 文件夹
temp = a.datas.copy(); a.datas.clear()
for dst, src, type in temp:
    c1 =  (dst == 'base_library.zip')                 # 判断文件是否为 base_library.zip
    c2 = any([dst.startswith(f) for f in my_folders]) # 判断文件是否属于 my_folders
    c3 = any([dst.startswith(f) for f in my_files])	  # 判断文件是否属于 my_files
    if any([c1, c2, c3]):
        a.datas.append((dst, src, type))
    else:
        a.datas.append((path.join('libs', dst), src, type))

# 把 a.binaries 中的二进制文件放到 a.datas ，作为普通文件复制到 libs 目录
for dst, src, type in a.binaries:
    c1 = (dst=='Python')                       # 不修改 Pyhton 
    c2 = re.fullmatch(r'python\d+\.dll', dst)  # 不修改 python310.dll
    if any([c1, c2]):
        # a.datas.append((dst, src, 'DATA'))
        a.datas.append((dst, src, type))
    else:
        # a.datas.append((path.join('libs', dst), src, 'DATA'))
        a.datas.append((path.join('libs', dst), src, type))
a.binaries.clear()

# 把所有的 py 文件依赖用 a.datas 复制到 libs 文件夹
# 可选地保留某些要打包的依赖
private_module = ['yys_main','yys_util','yys_config','ai_huijuan']                         # hello.exe 不保留任何依赖
temp = a.pure.copy(); a.pure.clear()
tmp = open('pure','w')
for name, src, type in temp:
    tmp.write('  '.join([name,src,type])+'\n')
    condition = [name.startswith(m) for m in private_module]
    # if condition and any(condition):
    if not any(condition):
        a.pure.append((name, src, type))    # 把需要保留打包的 py 文件重新添加回 a.pure
    else:
        # if 'win32' in name:
        #     print('---------------',name,src,type,'---------------')
        print('---------------',name,src,type,'---------------')
        name = name.replace('.', os.sep)
        init = path.join(name, '__init__.py')
        pos = src.find(init) if init in src else src.find(name)
        dst = src[pos:]
        dst = path.join('libs', dst)
        a.datas.append((dst, src, 'DATA'))  # 不需要打包的第三方依赖 py 文件引到 libs 文件夹

tmp.close()
# ========================为 a 生成 exe =========================

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='yys',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['xibai.ico'],
    contents_directory= '.'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='yys',
)
