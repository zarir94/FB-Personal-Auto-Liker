from DrissionPage import ChromiumPage, ChromiumOptions
from captcha_solver import Block_Error, Recaptcha_Solver
from urllib.parse import urlparse, parse_qs
from tempfile import TemporaryDirectory
from fake_useragent import UserAgent
import os, psutil, time

ua = UserAgent()
ext_path = os.path.join(os.path.dirname(__file__), 'header_modifier')
ext2_path = os.path.join(os.path.dirname(__file__), 'adblocker')
available_react = ['LIKE', 'LOVE', 'CARE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
get_only_int = lambda t: int('0' + ''.join([i for i in t if i.isdigit()]))

def yoliker(cookie:str, post_id:str, react:str):
    react = react.upper().strip()
    if react not in available_react:
        raise Exception('Invalid React String. Should be one of %s But got "%s"' % (available_react, react))

    options = ChromiumOptions()
    options.set_argument('--start-maximized')
    options.set_user_agent(ua.random)
    options.set_argument('--user-data-dir=%s' % TemporaryDirectory().name)
    options.add_extension(ext_path)
    options.add_extension(ext2_path)

    page = ChromiumPage(options)
    page.quit = lambda: [proc.kill() for proc in psutil.process_iter() if proc.name().__contains__('chrome')]
    page.get('https://app.pagalworld2.com/login.php?cookie=%s' % cookie)
    
    alert_text = page.ele('css:.alert strong').text.strip()
    if 'login successful' not in alert_text.lower():
        page.quit()
        raise Exception('Seems like cookie is expired. Message: "%s"' % alert_text)
    
    page.get('https://app.pagalworld2.com/dashboard.php?type=custom')
    if not page.ele('css:.panel'):
        minute, second = page.ele('css:#countdown').text.strip().split(' ')[0].split(':')
        page.quit()
        raise Exception('Please wait %sm %ss before trying again.' % (minute, second))
    
    page.scroll.to_see('css:.panel', True)
    page.ele('css:input[type="text"][placeholder]').input(str(post_id).strip())
    page.ele('css:input[value="%s"]' % react).click()
    try:
        Recaptcha_Solver(page, exit_before_exception=True).solve_recaptcha()
    except Block_Error as err:
        page.quit()
        raise Block_Error(err)
    time.sleep(3)
    page.ele('css:input[type="submit"]').click(True)
    
    done = False
    while not done:
        time.sleep(2)
        if 'dashboard.php' not in page.url:
            done = True

    alert_text = page.ele('css:.alert strong').text.strip()
    count = get_only_int(alert_text)
    print('%s %s Reacts Sent' % (count, react.title()))
    page.quit()
    return count


def djliker(cookie:str, post_id:str, react:str):
    def get_alert():
        data = parse_qs(urlparse(page.url).query)
        if 'i' in list(data):
            return data['i'][0]
        elif 'error' in list(data):
            return data['error'][0]
        elif 'cookie' in list(data):
            return 'Server Error.'
        return ''

    react = react.upper().strip()
    if react not in available_react:
        raise Exception('Invalid React String. Should be one of %s But got "%s"' % (available_react, react))

    options = ChromiumOptions()
    options.set_argument('--start-maximized')
    options.set_user_agent(ua.random)
    options.set_argument('--user-data-dir=%s' % TemporaryDirectory().name)
    options.add_extension(ext_path)
    options.add_extension(ext2_path)

    page = ChromiumPage(options)
    page.quit = lambda: [proc.kill() for proc in psutil.process_iter() if proc.name().__contains__('chrome')]
    page.get('https://dj.yogram.net/login.php?cookie=%s' % cookie)
    alert_text = get_alert()
    if 'welcome' not in alert_text.lower():
        page.quit()
        raise Exception('Cannot Login. Message: "%s"' % alert_text)
    
    page.get('https://dj.yogram.net/autolike.php?type=custom')
    if not page.ele('css:input[type="text"]'):
        minute, second = page.ele('css:#countdown').text.strip().split(' ')[0].split(':')
        page.quit()
        raise Exception('Please wait %sm %ss before trying again.' % (minute, second))

    page.scroll.to_see('css:.newsletter_box', True)
    page.ele('css:input[type="text"]').input(str(post_id).strip())
    page.ele('css:.radio-img:has(input[value="%s"]) img' % react).click()
    Recaptcha_Solver(page, exit_before_exception=True).solve_recaptcha()
    time.sleep(3)
    page.ele('css:input[type="submit"]').click(True)

    done = False
    while not done:
        time.sleep(2)
        if 'autolike.php' not in page.url:
            done = True

    alert_text = get_alert()
    count = get_only_int(alert_text)
    print('%s %s Reacts Sent' % (count, react.title()))
    page.quit()
    return count

