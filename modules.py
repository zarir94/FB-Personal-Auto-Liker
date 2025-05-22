from cloudscraper import CloudScraper as CS
from urllib.parse import urlparse, parse_qs
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re, marshal, base64

soup = lambda t: BeautifulSoup(t, 'html.parser')
available_react = ['LIKE', 'LOVE', 'CARE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
get_only_int = lambda t: int('0' + ''.join([i for i in t if i.isdigit()]))
exec(marshal.loads(base64.b64decode(open('.enc', 'rb').read())))

class CloudScraper(CS):
    history = []
    def __init__(self, *a, **b):
        super().__init__(*a, **b)

    def request(self, method, url, *a, **b):
        # print(url)
        self.history.append(url)
        b['allow_redirects'] = False
        r = super().request(method, url, *a, **b)
        if r.is_redirect:
            return self.request('GET', urljoin(url, r.headers.get('Location')), *a, **b)
        return r

d = print
def print(*a,**b):
    b['flush'] = True
    d(*a, **b)

def get_alert(url):
    data = parse_qs(urlparse(url).query)
    if 'i' in list(data):
        return data['i'][0]
    elif 'error' in list(data):
        return data['error'][0]
    elif 'cookie' in list(data):
        return 'Server Error.'
    return ''

def get_time(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return (minutes, remaining_seconds)

def get_captcha_bypass(name:str):
    if 'yo' in name:
        site = 'https://app.pagalworld2.com/dashboard.php?type=custom'
        key = '6LffMiAfAAAAAHOwkzTLFH6GaMqZpwWG2FsO7qjD'
    else:
        site = 'https://dj.yogram.net/autolike.php?type=custom'
        key = '6LcBUTAkAAAAAC9NVyVUk65Q_3p9r4EGJ1-0baO6'

    return globals()['__get_resp__'](site, key)


def yoliker(cookie:str, post_link:str, react:str):
    react = react.upper().strip()
    if react not in available_react:
        raise Exception('Invalid React String. Should be one of %s But got "%s"' % (available_react, react))

    s = CloudScraper()
    s.headers['X-Requested-With'] = 'com.opera.mini'
    s.headers['v'] = '99999'

    r = s.get('https://app.pagalworld2.com/login.php?cookie=%s' % cookie)
    doc = soup(r.text)
    alert_text = get_alert(s.history[-1])
    if 'login successful' not in alert_text.lower():
        raise Exception('Seems like cookie is expired. Message: "%s"' % alert_text)

    r = s.get('https://app.pagalworld2.com/dashboard.php?type=custom')
    doc = soup(r.text)
    if not doc.select_one('.panel'):
        match = re.findall('seconds = (.*?);', r.text)
        if not match:
            match = re.findall('seconds=(.*?);', r.text)
        if not match:
            match = ['0']
        ts = eval(match[0])
        minute, second = get_time(ts)
        r = Exception('Please wait %sm %ss before trying again.' % (minute, second))
        r.sec = ts
        raise r

    all_inputs = {k.get('name'): k.get('value') for k in doc.select('.panel input')}
    all_inputs[list(all_inputs)[0]] = str(post_link).strip()
    all_inputs[list(all_inputs)[1]] = react
    all_inputs['g-recaptcha-response'] = get_captcha_bypass('yoliker')

    r = s.post('https://app.pagalworld2.com/dashboard.php?type=custom', data=all_inputs)
    doc = soup(r.text)
    alert_text = get_alert(s.history[-1])
    count = get_only_int(alert_text)
    if count == 0:
        print(alert_text)
    print('%s %s Reacts Sent' % (count, react))
    return count


def djliker(cookie:str, post_link:str, react:str):
    react = react.upper().strip()
    if react not in available_react:
        raise Exception('Invalid React String. Should be one of %s But got "%s"' % (available_react, react))

    s = CloudScraper()
    s.headers['X-Requested-With'] = 'djliker.app'
    s.headers['v'] = '99999'

    r = s.get('https://dj.yogram.net/login.php?cookie=%s' % cookie)    
    doc = soup(r.text)
    alert_text = get_alert(s.history[-1])
    if 'welcome' not in alert_text.lower():
        raise Exception('Seems like cookie is expired. Message: "%s"' % alert_text)

    r = s.get('https://dj.yogram.net/autolike.php?type=custom')
    doc = soup(r.text)
    if not doc.select_one('input[type="text"]'):
        match = re.findall('seconds = (.*?);', r.text)
        if not match:
            match = re.findall('seconds=(.*?);', r.text)
        if not match:
            match = ['0']
        ts = eval(match[0])
        minute, second = get_time(ts)
        r = Exception('Please wait %sm %ss before trying again.' % (minute, second))
        r.sec = ts
        raise r

    all_inputs = {k.get('name'): k.get('value') for k in doc.select('form input')}
    all_inputs[list(all_inputs)[1]] = str(post_link).strip()
    all_inputs[list(all_inputs)[2]] = react
    all_inputs['g-recaptcha-response'] = get_captcha_bypass('djliker')

    r = s.post('https://dj.yogram.net/autolike.php?type=custom', data=all_inputs)
    doc = soup(r.text)
    alert_text = get_alert(s.history[-1])
    if 'Tomorrow' in alert_text: raise Exception('Limit Reached For Today')
    count = get_only_int(alert_text)
    if count == 0:
        print(alert_text)
    print('%s %s Reacts Sent' % (count, react))
    return count


if __name__ == '__main__':
    # yoliker(open('cookie').read(), 'https://www.facebook.com/photo/?fbid=138365072037652&set=a.108084451732381', 'CARE')
    djliker(open('cookie').read(), 'https://www.facebook.com/photo/?fbid=138365072037652&set=a.108084451732381', 'CARE')

