from selenium_recaptcha import Recaptcha_Solver
from seleniumbase.config import settings
from seleniumbase import Driver
from requests import get
from time import sleep
import os, sys, traceback

settings.HIDE_DRIVER_DOWNLOADS = True
ext_path = os.path.join(os.path.dirname(__file__), 'header_modifier')
available_react = ['LIKE', 'LOVE', 'CARE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
d=print

def print(*a, **kw):
    kw['flush'] = True
    d(*a, **kw)

def get_only_int(text:str) -> int:
    n = '0'
    for i in text:
        if i.isdigit():
            n+=i
    return int(n)

def yoliker(cookie:str, post_id:str, react:str):
    react = react.upper().strip()
    if react not in available_react:
        raise Exception('Invalid React String. Should be one of %s But got "%s"' % (available_react, react))
    driver = Driver(uc=True, ad_block_on=True, extension_dir=ext_path)
    driver.maximize_window()
    driver.get('https://app.pagalworld2.com/login.php?cookie=%s' % cookie)
    if 'error=' in driver.current_url:
        raise Exception('Looks Like Cookie is expired.')
    driver.get('https://app.pagalworld2.com/dashboard.php?type=custom')
    if not driver.is_element_present('.panel'):
        minute, second = driver.get_text('#countdown').split(' ')[0].split(':')
        raise Exception('Please wait %sm %ss before trying again.' % (minute, second))
    driver.type('input[type="text"]', str(post_id))
    driver.click('input[value="%s"]' % react)
    Recaptcha_Solver(driver).solve_recaptcha()
    driver.click('input[type="submit"]')
    done = False
    while not done:
        sleep(2)
        if 'dashboard.php' not in driver.current_url:
            done = True
    react_count = get_only_int(driver.current_url.split('i=')[-1].replace('%20', ' '))
    print('%s %s Reactions Sent.' % (react_count, react.capitalize()))
    driver.quit()
    return react_count


def djliker(cookie:str, post_id:str, react:str):
    react = react.upper().strip()
    if react not in available_react:
        raise Exception('Invalid React String. Should be one of %s But got "%s"' % (available_react, react))
    driver = Driver(uc=True, ad_block_on=True, extension_dir=ext_path)
    driver.maximize_window()
    driver.get('https://dj.yogram.net/login.php?cookie=%s' % cookie)
    if 'error=' in driver.current_url:
        raise Exception('Looks Like Cookie is expired.')
    if 'cookie=' in driver.current_url:
        raise Exception('Looks Like Server is busy. Try again later.')
    driver.get('https://dj.yogram.net/autolike.php?type=custom')
    if not driver.is_element_present('.newsletter_box'):
        minute, second = driver.get_text('#countdown').split(' ')[0].split(':')
        raise Exception('Please wait %sm %ss before trying again.' % (minute, second))
    driver.type('input[type="text"]', str(post_id))
    driver.click('.radio-img:has(input[value="%s"]) img' % react)
    driver.execute_script('document.querySelector("header").remove()')
    Recaptcha_Solver(driver).solve_recaptcha()
    driver.click('input[type="submit"]')
    driver.execute_script('''try{document.querySelector('input[type="submit"]').click()}catch{}''')
    done = False
    while not done:
        sleep(2)
        if 'autolike.php' not in driver.current_url:
            done = True
    react_count = get_only_int(driver.current_url.split('i=')[-1].replace('%20', ' '))
    print('%s %s Reactions Sent.' % (react_count, react.capitalize()))
    driver.quit()
    return react_count


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




