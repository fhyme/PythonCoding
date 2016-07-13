# __author__ = 'Albert'
import cookielib
import os

import urlparse
import cgi
import re
import posixpath
from bs4 import BeautifulSoup
import urllib
import urllib2

from multiprocessing import Pool, cpu_count, freeze_support, Value
from multiprocessing.pool import ApplyResult
from copy_reg import pickle
from types import MethodType


def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)


def _unpickle_method(func_name, obj, cls):
    global func
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)


class Download:
    def __init__(self, email, password, course):
        a = Account(email, password)
        self.course = course
        self.html = a.getCourse(course)
        self.cookie = "cookie"
        self.links = []

    def getLinks(self, html):
        soup = BeautifulSoup(html, "lxml")
        links = soup.find_all('a', target='_new')
        print "All Links: ", len(links)
        self.links = [link['href'] for link in links]

    def _download(self, url):
        cookie = cookielib.MozillaCookieJar()
        cookie.load(self.cookie)
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookie)
        ]
        opener = urllib2.build_opener(*handlers)
        try:
            print "Start: ", url
            u = opener.open(url)
            file_size = int(u.headers.get("Content-Length", 0))
            _, params = cgi.parse_header(u.headers.get('Content-Disposition', ''))
            file_name = params.get('filename')
            if file_name is None:
                path = urlparse.urlsplit(url).path
                file_name = posixpath.basename(path)
            file_name = re.sub(r"[\\|/|\*|\?|:]", '-', urlparse.unquote(file_name))
            url = u.geturl()
            if os.path.exists(file_name):
                print file_name, ' already exist, continue...'
            else:
                print "Downloading: %s Bytes: %s" % (file_name, file_size)
                urllib.urlretrieve(url, file_name)
                print "Finish: %s" % file_name
        except Exception as e:
            print e

    def __call__(self, url):
        self._download(url)
        print "Succ: ", url

    def __del__(self):
        print "... Destructor"

    def download(self, workers=cpu_count()):
        self.getLinks(self.html)

        pool = Pool(processes=workers)
        pool.map(self, self.links)
        pool.close()
        pool.join()


if __name__ == "__main__":
    from config import USER
    from coursera import Account
    # pickle(MethodType, _pickle_method, _unpickle_method)
    d = Download(USER['email'], USER['password'], USER['course'])
    d.download()
