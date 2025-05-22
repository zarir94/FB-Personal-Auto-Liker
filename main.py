import traceback, sys
from requests import get
from modules import djliker, yoliker
from time import sleep

d = print
def print(*a,**b):
    b['flush'] = True
    d(*a, **b)

if __name__ == '__main__':
    post_link = sys.argv[1]
    amount = int(sys.argv[2])
    react = sys.argv[3]
    r = get('https://pastebin.com/raw/zNsX8viB')
    data = r.json()
    total_sent = 0
    while total_sent < amount:
        to_sleep = 1
        for name, cookie in data.items():
            print('=' * 60)
            print('[+] Trying %s in Yo Liker' % name)
            try:
                ins_yo = yoliker(cookie, post_link, react)
                total_sent += ins_yo
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as err:
                if 'wait' in str(err) and err.sec > to_sleep: to_sleep = err.sec
                print('\n'.join(traceback.format_exc().splitlines()[-3:]))
            print('\n[+] Trying %s in DJ Liker' % name)
            try:
                ins_dj = djliker(cookie, post_link, react)
                total_sent += ins_dj
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as err:
                if 'wait' in str(err) and err.sec > to_sleep: to_sleep = err.sec
                print('\n'.join(traceback.format_exc().splitlines()[-3:]))
            print('\n' * 3)
        
        print('Sleeping', to_sleep, 'Seconds...')
        sleep(to_sleep + 30)