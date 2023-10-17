import socket,time
s = socket.socket()
s.bind(('0.0.0.0',33333))
s.listen(300)

def check_time(time_list:list[list[socket.socket, float]]):
    tmp_list = time_list.copy()
    for i in time_list: # type: int
        if time.time()-i[1] > 30:
            i[0].close()
            tmp_list.remove(i)
    return tmp_list

time_list:list[list[socket.socket, float]] = []
while True:
    c = s.accept()
    time_list.append([c[0],time.time()])
    c[0].settimeout(3)
    try:
        choose = c[0].recv(10).decode().strip()
        if choose == 'update':
            tmp_buff = open('./version','r',encoding='utf-8')
        elif choose == 'user':
            tmp_buff = open('./yys_name','r',encoding='utf-8')
        c[0].sendall(tmp_buff.read().encode('utf-8'))
        tmp_buff.close()
    except Exception as e:
        print(e)
    
    time_list = check_time(time_list)
