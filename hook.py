import sys,os

# BASE_DIR = pathlib.Path(__file__).parent

# print(BASE_DIR)
print(sys.path)
print(f'\n\n模块查找路径：')
cur_path = os.getcwd()
# cur_path = cur_path[0].upper() + cur_path[1:]
print(cur_path)
for p in sys.path.copy():
    relative_p = p.replace(cur_path,'')
    # relative_p = pathlib.Path(p).relative_to(BASE_DIR)
    new_p = cur_path + '\\libs' + relative_p
    sys.path.insert(0, str(new_p))

win32_path = ['win32','pythonwin','pywin32_system32']
for p in win32_path:
    relative_p = p.replace(cur_path,'')
    # relative_p = pathlib.Path(p).relative_to(BASE_DIR)
    new_p = cur_path + '\\libs\\' + relative_p
    sys.path.insert(0, str(new_p))
for _ in range(sys.path.count(cur_path)):
    sys.path.remove(cur_path)
for i in sys.path:
    print(i)
print('\n')
