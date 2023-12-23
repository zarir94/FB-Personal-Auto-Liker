import traceback, sys
from requests import get
from modules import djliker, yoliker

if __name__ == '__main__':
    post_id = sys.argv[1]
    amount = int(sys.argv[2])
    react = sys.argv[3]
    r = get('https://pastebin.com/raw/zNsX8viB')
    data = r.json()
    total_sent = 0
    while total_sent < amount:
        for name, cookie in data.items():
            print('=' * 60)
            print('[+] Trying %s in Yo Liker' % name)
            try:
                ins_yo = yoliker(cookie, post_id, react)
                total_sent += ins_yo
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print(traceback.format_exc())
            print('\n[+] Trying %s in DJ Liker' % name)
            try:
                ins_dj = djliker(cookie, post_id, react)
                total_sent += ins_dj
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print(traceback.format_exc())
            print('\n' * 3)

