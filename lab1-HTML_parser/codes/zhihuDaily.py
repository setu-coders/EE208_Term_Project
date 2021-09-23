# SJTU EE208

import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def parseZhihuDaily(content, url):
    zhihulist = list()
    soup = BeautifulSoup(content, features = "html.parser")
    masterurl = "http://daily.zhihu.com/"
    for i in soup.findAll('a',{'href':re.compile('/story/.')}): # i: everything inside <a> </a>
        storyurl = i.get('href','')
        imgurl = i.find('img').get('src','')
        titleElement = i.contents[1]    # child 1
        titlestr = titleElement.string  # zhihu doesn't use <title>, but <span>, so element.string is used
        zhihulist.append([imgurl,titlestr,(masterurl + storyurl)])

    return zhihulist


def write_outputs(zhihus, filename):
    file = open(filename, "w", encoding='utf-8')
    for zhihu in zhihus:
        for element in zhihu:
            file.write(element)
            file.write('\t')
        file.write('\n')
    file.close()


def main():
    url = "http://daily.zhihu.com/"
    content = urllib.request.urlopen(url).read()
    zhihus = parseZhihuDaily(content, url)
    write_outputs(zhihus, "res3.txt")


if __name__ == '__main__':
    main()
