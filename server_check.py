import socket
s = socket.socket()
s.bind(('0.0.0.0',33333))
s.listen(300)
while True:
    c = s.accept()
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
        c[0].close()