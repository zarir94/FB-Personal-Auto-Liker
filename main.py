from selenium_recaptcha.components import find_until_located, find_until_clicklable
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium_recaptcha import Recaptcha_Solver
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
from seleniumwire import webdriver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from time import sleep
from base64 import b64decode


def get_msg_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    try:
        return parse_qs(parsed_url.query)['i'][0]
    except:
        print('Got url:', url, flush=True)
        return ''


def interceptor(request):
    if 'pagead2.googlesyndication.com' in request.url:
        request.abort()
    request.headers['X-Requested-With'] = 'com.instagram.android'


def get_int(text: str) -> int:
    number = ''
    for letter in text:
        if letter.isdigit():
            number += letter
    if number == '':
        raise Exception('No Integer Found')
    return int(number)


def YoLiker_Bot(proxy:str, react: str, post_id: str, cookie: str, headless=True):
    url = f"http://app.pagalworld2.com/login.php?access_token=&cookie={quote_plus(cookie)}"
    all_reacts = ['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
    if not react in all_reacts:
        raise Exception(
            f'Invalid Reaction Name. Please be sure that the value is in {all_reacts}')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

    #print("Downloading Webdriver", flush=True)
    #service = Service(ChromeDriverManager().install())
    #print("Done Downloading", flush=True)

    driver = webdriver.Chrome(chrome_options=options, service_log_path="NUL", seleniumwire_options = {'proxy': {'http': proxy}})
    driver.set_window_size(400, 700)
    driver.request_interceptor = interceptor

    driver.get(url)
    print("Openning URL", flush=True)

    if not 'Login Successful' in get_msg_from_url(driver.current_url):
        driver.close()
        raise Exception('Could Not Login, Please check your Cookie')
    print("Login Successful", flush=True)

    driver.get('http://app.pagalworld2.com/dashboard.php?type=custom')

    sleep(1)

    try:
        driver.execute_script(
            "document.querySelector('.panel').scrollIntoView(true);")
        sleep(1)
    except:
        cd_text = driver.find_element(By.ID, 'countdown').text
        time = cd_text.split(' ')
        minutes = time[0].split(':')[0]
        seconds = time[0].split(':')[1]
        driver.close()
        raise Exception(f'Remaining Time {minutes} minutes {seconds} seconds.')
    print("Solving Captcha", flush=True)
    try:
        solver = Recaptcha_Solver(driver, 'ffmpeg.exe')
        solver.solve_recaptcha()
    except Exception as e:
        driver.close()
        raise Exception(f'Could not solve Captcha! Error: {e}')
    print("Filling up form", flush=True)

    input_form = find_until_located(
        driver, By.CSS_SELECTOR, 'input[type=text]')
    input_form.send_keys(post_id)
    sleep(1)

    find_until_located(driver, By.CSS_SELECTOR,
                       f'input[type=radio][value={react}]').click()
    sleep(1)

    find_until_clicklable(driver, By.CSS_SELECTOR,
                          'input[type=submit]').click()
    sleep(5)

    response_text = find_until_located(
        driver, By.CSS_SELECTOR, '.alert strong').text
    try:
        sent_react = get_int(response_text)
    except:
        driver.close()
        raise Exception(
            f'Something Went wrong after submit. Error: {response_text}')

    driver.close()
    return {'react': sent_react, 'react_type': react}


def DJLiker_Bot(proxy:str, react: str, post_id: str, cookie: str, headless=True):
    url = f"http://app.fbliker.net/login.php?access_token=&cookie={quote_plus(cookie)}"
    all_reacts = ['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
    if not react in all_reacts:
        raise Exception(
            f'Invalid Reaction Name. Please be sure that the value is in {all_reacts}')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

    #print("Downloading Webdriver", flush=True)
    #service = Service(ChromeDriverManager().install())
    #print("Done Downloading", flush=True)

    driver = webdriver.Chrome(chrome_options=options, service_log_path="NUL", seleniumwire_options = {'proxy': {'http': proxy}})
    driver.set_window_size(400, 700)
    driver.request_interceptor = interceptor

    driver.get(url)
    print("Openning URL", flush=True)
    # if 'Just a moment' in driver.title:
    #     sleep(60)

    if not 'Welcome' in get_msg_from_url(driver.current_url):
        driver.close()
        raise Exception('Could Not Login, Please check your Cookie')
    print("Login Successful", flush=True)

    driver.get('http://app.fbliker.net/autolike.php?type=custom')

    sleep(1)

    try:
        driver.execute_script(
            "document.querySelector('input[type=text]').scrollIntoView(true);")
        sleep(1)
    except:
        cd_text = driver.find_element(By.ID, 'countdown').text
        time = cd_text.split(' ')
        minutes = time[0].split(':')[0]
        seconds = time[0].split(':')[1]
        driver.close()
        raise Exception(f'Remaining Time {minutes} minutes {seconds} seconds.')
    print("Solving Captcha", flush=True)
    try:
        solver = Recaptcha_Solver(driver, 'ffmpeg.exe')
        solver.solve_recaptcha()
    except Exception as e:
        driver.close()
        raise Exception(f'Could not solve Captcha! Error: {e}')
    print("Filling up form", flush=True)

    input_form = find_until_located(
        driver, By.CSS_SELECTOR, 'input[type=text]')
    input_form.send_keys(post_id)
    sleep(1)

    find_until_located(driver, By.CSS_SELECTOR, f'input[value={react}]')\
        .find_element(By.XPATH, '..')\
        .click()
    sleep(1)

    find_until_clicklable(driver, By.CSS_SELECTOR,
                          'input[type=submit]').click()
    sleep(5)

    response_text = get_msg_from_url(driver.current_url)
    try:
        sent_react = get_int(response_text)
    except Exception as e:
        driver.close()
        raise Exception(
            f'Something Went wrong after submit. Error: {response_text} Exception: {e}')

    driver.close()
    return {'react': sent_react, 'react_type': react}



if __name__ == '__main__':
    # FILE.PY REACT POST_ID COOKIE
    # main.py LOVE 1937183719392 fb_cookie
    import sys
    proxy = 'http://' + sys.argv[1]
    react = sys.argv[2]
    post_id = sys.argv[3]
    cookies = sys.argv[4:]
    print("Got Everything", flush=True)
    while True:
        for cookie in cookies:
            cookie=b64decode(cookie).decode()
            print(f"React: {react}\nID: {post_id}\nCookie: {cookie}", flush=True)
            yo_error=0
            dj_error=0
            print("Trying DJ", flush=True)
            while True:
                try:
                    DJ=DJLiker_Bot(proxy, react, post_id, cookie)
                    DJ_react=DJ['react']
                    DJ_react_type=DJ['react_type']
                    print(f'{DJ_react} {DJ_react_type} Reacts Sent', flush=True)
                    break
                except Exception as e1:
                    if 'Could not solve Captcha' in str(e1) and dj_error < 9:
                        print(f'Could not solve captcha at DJ Liker...\nError: {str(e1)} Retrying...', flush=True)
                        dj_error+=1
                        continue
                    else:
                        print(f'Error at DJ Liker: \n{str(e1)}\nSkipping This Time...', flush=True)
                        break
            print("Trying YO", flush=True)
            while True:
                try:
                    YO=YoLiker_Bot(proxy, react, post_id, cookie)
                    YO_react=YO['react']
                    YO_react_type=YO['react_type']
                    print(f'{YO_react} {YO_react_type} Reacts Sent', flush=True)
                    break
                except Exception as e1:
                    if 'Could not solve Captcha' in str(e1) and yo_error < 9:
                        print(f'Could not solve captcha at YO Liker...\nError: {str(e1)} Retrying...', flush=True)
                        yo_error+=1
                        continue
                    else:
                        print(f'Error at YO Liker: \n{str(e1)}\nSkipping This Time...', flush=True)
                        break
        sleep(60 * 35)
