from cloudscraper import CloudScraper as CS
from urllib.parse import urljoin

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

s = CloudScraper()

s.get('https://dj.yogram.net/login.php?cookie=helo')
s.get('http://google.com')
s.get('http://tiny.cc/shellvnc')
# print(r.text)
print(s.history)



