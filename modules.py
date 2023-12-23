from cloudscraper import CloudScraper as CS
from urllib.parse import urlparse, parse_qs
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import capsolver, re

soup = lambda t: BeautifulSoup(t, 'html.parser')
available_react = ['LIKE', 'LOVE', 'CARE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
get_only_int = lambda t: int('0' + ''.join([i for i in t if i.isdigit()]))
capsolver.api_key = 'CAP-FC7EF960A66611179C9835150DB4605D'


class CloudScraper(CS):
    history = []
    def __init__(self, *a, **b):
        super().__init__(*a, **b)

    def request(self, method, url, *a, **b):
        self.history.append(url)
        b['allow_redirects'] = False
        r = super().request(method, url, *a, **b)
        if r.is_redirect:
            return self.request('GET', urljoin(url, r.headers.get('Location')), *a, **b)
        return r

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
    def __get_resp__(url, key):
        solution = capsolver.solve({
                "type":"ReCaptchaV2TaskProxyLess",
                "websiteKey": key,
                "websiteURL": url,
            })
        token = solution['gRecaptchaResponse']
        return token

    if 'yo' in name:
        site = 'https://app.pagalworld2.com/dashboard.php?type=custom'
        key = '6LffMiAfAAAAAHOwkzTLFH6GaMqZpwWG2FsO7qjD'
    else:
        site = 'https://dj.yogram.net/autolike.php?type=custom'
        key = ''

    return __get_resp__(site, key)


def yoliker(cookie:str, post_id:str, react:str):
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
        minute, second = get_time(eval(match[0]))
        raise Exception('Please wait %sm %ss before trying again.' % (minute, second))
    
    all_inputs = {k.get('name'): k.get('value') for k in doc.select('.panel input')}
    all_inputs[list(all_inputs)[0]] = str(post_id).strip()
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


def djliker(cookie:str, post_id:str, react:str):
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

    r = s.get('https://app.pagalworld2.com/dashboard.php?type=custom')
    doc = soup(r.text)
    if not doc.select_one('.panel'):
        match = re.findall('seconds = (.*?);', r.text)
        if not match:
            match = re.findall('seconds=(.*?);', r.text)
        if not match:
            match = ['0']
        minute, second = get_time(eval(match[0]))
        raise Exception('Please wait %sm %ss before trying again.' % (minute, second))
    
    all_inputs = {k.get('name'): k.get('value') for k in doc.select('.panel input')}
    all_inputs[list(all_inputs)[0]] = str(post_id).strip()
    all_inputs[list(all_inputs)[1]] = react
    all_inputs['g-recaptcha-response'] = get_captcha_bypass('yoliker')

    r = s.post('https://app.pagalworld2.com/dashboard.php?type=custom', data=all_inputs)
    doc = soup(r.text)
    alert_text = doc.select_one('.alert strong').text.strip()
    count = get_only_int(alert_text)
    if count == 0:
        print(alert_text)
    print('%s %s Reacts Sent' % (count, react))
    return count


yoliker(open('cookie').read(), '374898821717608', 'LOVE')
# djliker(open('cookie').read(), '374898821717608', 'LOVE')

