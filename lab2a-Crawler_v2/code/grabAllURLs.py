# SJTU EE208

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    soup = BeautifulSoup(content, features = "html.parser")
    for i in soup.findAll('a'):
        url = i.get('href','') 
        urlset.add(url)
   

    return urlset


def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()


def main():
    url = "https://www.baidu.com"
    content = urllib.request.urlopen(url).read()
    print(str(content))
    """
    urlSet = parseURL(content)
    write_outputs(urlSet, "res1.txt")
    """

if __name__ == '__main__':
    main()
