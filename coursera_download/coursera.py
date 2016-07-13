# __author__ = 'Albert'

import urllib
import urllib2
import cookielib


class Account:
    def __init__(self, uid, passwd):
        self.uid = uid
        self.passwd = passwd

        self.csrf3_token = ''
        self.cookie = cookielib.MozillaCookieJar("cookie")

        self.links = []

        self.start()

    def get_csrf3_token(self):
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(self.cookie)
        ]
        opener = urllib2.build_opener(*handlers)
        index = "https://www.coursera.org/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
        }
        req = urllib2.Request(index, headers=headers)
        u = opener.open(req)
        for cookie in self.cookie:
            if cookie.name == 'CSRF3-Token':
                self.csrf3_token = cookie.value
        opener.close()

    def getCookie(self):
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(self.cookie)
        ]
        opener = urllib2.build_opener(*handlers)
        login_url = "https://www.coursera.org/api/login/v3Ssr?csrf3-token=" + self.csrf3_token
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
            'Referer': 'https://www.coursera.org/?authMode=login',
            'Cookie': 'CSRF3-Token=' + self.csrf3_token
        }
        formData = {
            'email': self.uid,
            'password': self.passwd
        }
        req = urllib2.Request(login_url, urllib.urlencode(formData), headers)
        u = opener.open(req)
        opener.close()

    def getCourse(self, course_name):
        url = "https://class.coursera.org/%s/lecture" % course_name
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(self.cookie)
        ]
        opener = urllib2.build_opener(*handlers)
        u = opener.open(url)
        return u.read()

    def start(self):
        self.get_csrf3_token()
        print "Get csrf3_token:", self.csrf3_token
        self.getCookie()
        print "Get cookie:", self.cookie
        self.cookie.save()

