from urllib import request, parse, error
import json
import http.cookiejar

def url_get():
    base_url = 'https://www.runoob.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36',
        'accept': 'text/html'
    }
    params = {
        's': 'python'
    }

    url = base_url + '?'+parse.urlencode(params)
    req = request.Request(url, headers=headers, method='GET')

    try:
        resp = request.urlopen(req)
    except error.HTTPError as http_err:
        print(http_err)
    except error.URLError as url_err:
        print(url_err)
    else:
        print(resp.status)
        print(resp.headers["Content-Type"])
        # print(resp.read().decode("utf-8"))


def url_post():
    base_url = 'https://developer.mozilla.org/pong/get'
    headers = {
        "Content-Type": "application/json"
    }
    # data =parse.urlencode({
    #         "keywords":[],
    #         "pongs": ["side", "top", "bottom"]
    #     }).encode('utf-8')

    data = json.dumps({
        "keywords": [],
        "pongs": ["side", "top", "bottom"]
    }).encode('utf-8')

    req = request.Request(base_url, data=data, headers=headers, method='POST')
    cookie_jar = http.cookiejar.MozillaCookieJar('cookies.txt')
    handle =request.HTTPCookieProcessor(cookie_jar)
    openner = request.build_opener(handle)
    try:
        # resp = request.urlopen(req)
        resp = openner.open(req)
    except error.HTTPError as http_err:
        print(http_err)
    except error.URLError as url_err:
        print(url_err)
    else:
        print(resp.status)
        print(resp.headers["Content-Type"])
        print(resp.info())
        print(json.loads(resp.read().decode('utf-8')))


if __name__ == '__main__':
    url_post()