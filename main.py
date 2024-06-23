import traceback, sys
from requests import get
from modules import djliker, yoliker
from time import sleep, time

d = print
def print(*a,**b):
    b['flush'] = True
    d(*a, **b)

if __name__ == '__main__':
    post_id = sys.argv[1]
    amount = int(sys.argv[2])
    react = sys.argv[3]
    r = get('https://pastebin.com/raw/zNsX8viB')
    data = r.json()
    total_sent = 0
    last_yoliker_run = last_djliker_run = 0
    yoliker_timelimit = 30 * 60 # 30 mins
    djliker_timelimit = 15 * 60 # 15 mins
    safety_limit = 60 # 1 min
    while total_sent < amount:
        for name, cookie in data.items():
            print('=' * 60)
            if time() > last_yoliker_run + yoliker_timelimit + safety_limit:
                print('[+] Trying %s in Yo Liker' % name)
                try:
                    ins_yo = yoliker(cookie, post_id, react)
                    total_sent += ins_yo
                    last_yoliker_run = time()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except Exception as err:
                    print('\n'.join(traceback.format_exc().splitlines()[-3:]))
            else: print('[-] Skipping Yo Liker since time limit not passed.')
            if time() > last_djliker_run + djliker_timelimit + safety_limit:
                print('\n[+] Trying %s in DJ Liker' % name)
                try:
                    ins_dj = djliker(cookie, post_id, react)
                    total_sent += ins_dj
                    last_djliker_run = time()
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except Exception as err:
                    print('\n'.join(traceback.format_exc().splitlines()[-3:]))
            else: print('[-] Skipping DJ Liker since time limit not passed.')
            print('\n' * 3)
        
        print('Sleeping 15 minutes...')
        sleep(15 * 60)

