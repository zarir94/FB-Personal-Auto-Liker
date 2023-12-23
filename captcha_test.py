from requests import post
import capsolver

capsolver.api_key = 'CAP-FC7EF960A66611179C9835150DB4605D'

print(capsolver.balance())

solution = capsolver.solve({
        "type":"ReCaptchaV2TaskProxyLess",
        "websiteKey":"6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        "websiteURL":"https://www.google.com/recaptcha/api2/demo",
    })

token = solution['gRecaptchaResponse']
print(token)

r = post('https://www.google.com/recaptcha/api2/demo', data={'g-recaptcha-response': token})

if 'Please verify that you are not a robot.' in r.text:
    print('Recatpcha Not Passed')
else:
    print(r.text)

