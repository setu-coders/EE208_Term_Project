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
import threading
import queue
import time
from bs4 import BeautifulSoup
from bloomFilter import BloomFilter  # 自己实现的BloomFilter类

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-thread")
parser.add_argument("-page")
args = parser.parse_args()


 
TIMEOUTSECONDS = 5  #访问超时时间
MAXFILENAMELENGTH = 50  #文件名最长不超过的长度
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
        return content.decode(coding)



def get_all_links(content, page):  # html content, page url
    
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for href_tag in soup.findAll("a",{"href" : re.compile("^http|^/|")}):
        url = href_tag.get("href","")
        
       
        if url[:4] != "http":
            url = urllib.parse.urljoin(page,url) 
        links.append(url)
        

    return links


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
    f = open(os.path.join(folder, filename), 'w')
    f.write(str(content))
    f.close()

count = 0
MAXCOUNT = 50
def crawl():
    while True:
        
        page = q.get(block = True,timeout = TIMEOUTSECONDS)
       
        if not crawled.find(page):
            #print("current page:",page)
            try:
                print("getting:",page)
                content = get_page(page)
            except ValueError:
                print(page,"not found or cannot open!")
                q.task_done()                 #    访问url失败时也要调用queue.task_done()
                continue
            
            
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            #print(outlinks)
            global count
            for link in outlinks:
                if (not crawled.find(link)) and count < MAXCOUNT :
                    q.put(link)
                    count += 1
            if varLock.acquire():
                graph[page] = outlinks
                crawled.add(page)
                varLock.release()
        print("Tasks left:",q.qsize())
        q.task_done()
        
    
            



if __name__ == '__main__':

    seed = str(sys.argv[1])
    #method = sys.argv[2]
    #max_page = int(sys.argv[3])

    start_time = time.time()    # 计时器

    THREAD_NUM = 8       # 线程数
    
    varLock = threading.Lock()
    q = queue.Queue()

    

    
    crawled = BloomFilter(10000,5)
    graph = {}

    q.put(seed)
    for i in range(THREAD_NUM):
        t = threading.Thread(target=crawl)
        t.daemon = True
        t.start()
    
    print("Start Working!")
    q.join()            # 等待queue为空
    
    
    
    end_time = time.time()
    print(f"total time used:{(end_time - start_time)}")
