# SJTU EE208
# -*-coding:utf-8-*-
import os
import re
import string
import sys
import urllib
#import urllib.error
import urllib.parse
import urllib.request
import hashlib

from bs4 import BeautifulSoup

MAXFILENAMELENGTH = 50 
TIMEOUTSECONDS = 5


def valid_filename(s):
    valid_chars = "-_(). %s%s" % (string.ascii_letters, string.digits)  
    s = ''.join((c if c != '.' else '+') for c in s if c in valid_chars)    # 去掉文件名.
    return s[:MAXFILENAMELENGTH] + '.html'    # 防止文件名过长


def get_page(page,coding = 'utf-8'):
    
    try:
        content = urllib.request.urlopen(page,timeout=TIMEOUTSECONDS).read()
    except:
        raise ValueError
    else:
        return content.decode(coding) # 用指定的编码方式解码，防止html乱码



def get_all_links(content, page):  # html content, page url
    
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for href_tag in soup.findAll("a",{"href" : re.compile("^http|^/|")}):
        url = href_tag.get("href","")
        
       
        if url[:4] != "http":
            url = urllib.parse.urljoin(page,url) 
        links.append(url)
        

    return links


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)    #元素入栈


def union_bfs(a, b):
    for e in b:
        if e not in a:
            a.insert(0,e)   # 元素入队


def add_page_to_folder(page, content):  
    index_filename = 'index.txt'  
    folder = 'html' 
    filename = valid_filename(page)  
    #print(filename)
    index = open(index_filename, 'a')
    index.write(str(page) + '\t' + str(filename) + '\n')
    index.close()
    #print(page_link)
    if not os.path.exists(folder):  
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w',encoding='utf-8')
    f.write(str(content))
    f.close()


def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0

    while tocrawl and count < max_page:
        page = tocrawl.pop()
        if page not in crawled and page:
            #print("current page:",page)
            try:
                content = get_page(page)
            except ValueError:
                print(page,"not found or cannot open!")
                continue
            else:
                print(page)
           
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            graph[page] = outlinks
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)

            count += 1

    return graph, crawled


if __name__ == '__main__':

    seed = str(sys.argv[1])
    method = sys.argv[2]
    max_page = int(sys.argv[3])

    graph, crawled = crawl(seed, method, max_page)
    #print(visitedlinks)
    
