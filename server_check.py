import socket
s = socket.socket()
s.bind(('0.0.0.0',33333))
s.listen(300)
while True:
    c = s.accept()
    tmp_buff = open('./yys_name','r',encoding='utf-8')
    c[0].sendall(tmp_buff.read().encode('utf-8'))
    tmp_buff.close()