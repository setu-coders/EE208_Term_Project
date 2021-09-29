# SJTU EE208
# -*-coding:utf-8-*-
import os
import math
import re
import string
import sys
from urllib.request import Request, urlopen
from urllib.request import Request, urlopen
url = 'http://tieba.baidu.com/f?fr=wwwt'
headers = {'User-Agent': 'Mozilla/5.0'}
request = Request(url, headers=headers)
html = urlopen(request).read()
print(html)
