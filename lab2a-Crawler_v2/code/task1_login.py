# SJTU EE208
# -*-coding:utf-8-*-
import re
import urllib.parse
import urllib.request
from http import cookiejar

from bs4 import BeautifulSoup
from urllib.request import urlopen

import ssl  
ssl._create_default_https_context = ssl._create_unverified_context    #不加这个会报错(SSL)


# 1. 构建一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
# 2. 使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
# 3. 通过build_opener()来构建opener
opener = urllib.request.build_opener(cookie_handler)
# 4. addheaders接受一个列表，里面每个元素都是一个headers信息的元组，opener附带headers信息
opener.addheaders = [("User-Agent", "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, \
                       like Gecko) Chrome/58.0.3029.110Safari/537.36")]
# 5. 需要登陆的账号和密码, 此处需要使用你们自己注册的账号密码
data = {"username": "_Asuka_",
        "pwd": "vNVtAVmSk3gYhE8",
        "formhash": "4A95C39D38",
        "backurl": "https%3A%2F%2Fwww.yaozh.com%2F"}

sign_in_url = "https://www.yaozh.com/login/"
info_url = "https://www.yaozh.com/member/basicinfo/"
# 6. 通过urlencode转码
postdata = urllib.parse.urlencode(data).encode("utf8")
# 7. 构建Request请求对象，包含需要发送的用户名和密码
request = urllib.request.Request(sign_in_url, data=postdata,headers = dict(Referer = sign_in_url))
# 8. 通过opener发送这个请求，并获取登陆后的Cookie值

opener.open(request)
response = opener.open(info_url).read()
soup = BeautifulSoup(response,features="html.parser")
myinfo = soup.find("div",{"class":"U_myinfo clearfix"})
#print(myinfo)
contents = myinfo.contents
#print(contents[3].find("input").get("value",""))
#print(contents[5].find("input").get("value",""))
needed_info = [
        contents[i].find("input").get("value","") for i in [3,5,7,9]
]
needed_info.append(contents[11].find("textarea").string)
#print(needed_info)

print(f"\
真实姓名：{needed_info[0]}\n\
用户名：{needed_info[1]} \n\
性别：{needed_info[2]} \n\
出生年月：{needed_info[3]}\n\
简介：{needed_info[4]}\
")
# The rest is done by you: