# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

ZHIHU_URL = 'http://www.zhihu.com/'
LOGIN_URL = ZHIHU_URL + 'login/email'
LOGOUT_URL = ZHIHU_URL + 'logout'
CAPTCHA_URL = ZHIHU_URL + 'captcha.gif'
COOKIES_FILENAME = 'cookies.json'
HEADERS = {"Accept": "*/*",
           "origin": "http://www.zhihu.com/",
           "Host": "www.zhihu.com",
           "Referer": "http://www.zhihu.com/",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36"}

class zhihu(object):
    def __init__(self):
        self._session = requests.session()

    #get xsrf
    #BeautifulSoup is needed, return xsrf string
    def get_xsrf(self, url=LOGIN_URL):
        r = self._session.get(url, headers=HEADERS)
        xsrf = BeautifulSoup(r.content, "lxml").find(type='hidden')['value']
        if xsrf is None:
            return ''
        else:
            return xsrf
    
    #get captcha
    #return captcha string
    def get_captcha(self, url=CAPTCHA_URL):
        captcha = self._session.get(url, stream=True)
        print captcha
        f = open('captcha.gif', 'wb')
        for line in captcha.iter_content(10):
            f.write(line)
        f.close()
        print u'input captcha:'
        captchastr = raw_input()
        return captchastr

    #login
    def login(self, url=LOGIN_URL, account='', password='', 
              captcha='', savecookies=True, headers=HEADERS):
        xsrf = self.get_xsrf()
        captcha = self.get_captcha()
        logindata = {'_xsrf': xsrf,
                     'captcha': captcha,
                     'email': account,
                     'password': password,
                     'rememberme': 'true'}
        res = self._session.post(url, data=logindata, headers=headers)
        print res.text
        #j = res.json()
        #c = int(j['r'])
        #m = j['msg']
        #if c == 0 and savecookies is True:
            #with open(self.cookies_filename, 'w') as f:
                #json.dump(self.session.cookies.get_dict(), f)
        #return c, m
        
    #logout
    def logout(self, url=LOGOUT_URL, headers=HEADERS):
        res = self._session.get(url, headers=headers)
        print res.text 
 
