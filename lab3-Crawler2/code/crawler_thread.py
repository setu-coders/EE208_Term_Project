# SJTU EE208
# -*-coding:utf-8-*-
import os
import math
import re
import string
import sys
from typing import final
import urllib
import urllib.error
import urllib.parse
import urllib.request
from urllib.request import Request, urlopen
import hashlib
import threading
import queue
import time
from bs4 import BeautifulSoup
import argparse
import bloomFilter  # 自己实现的BloomFilter类


TIMEOUTSECONDS = 3 #访问超时时间
MAXFILENAMELENGTH = 50  #文件名最长不超过的长度
SELF_URL_MARKER  = "SELF_URL_TAG:"   # 爬取到的网页写入文件时，在html文件末尾附上该网页的url方便查询

header = {'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54'}

def valid_filename(s):
    valid_chars = "-_(). %s%s" % (string.ascii_letters, string.digits)  
    s = ''.join((c if c != '.' else '+') for c in s if c in valid_chars)    # 去掉文件名.
    return s[:MAXFILENAMELENGTH] + '.html'    # 防止文件名过长


def get_page(page,coding = 'utf-8'):
    global successful
    global failed
    try:
        request = Request(page, headers=header)
        content = urlopen(request,timeout = TIMEOUTSECONDS).read()
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
    folder = 'html_2' 
    filename = valid_filename(page)  
    #print(filename)
    index = open(index_filename, 'a')
    index.write(str(page) + '\t' + str(filename) + '\n')
    index.close()
    #print(page_link)
    if not os.path.exists(folder):  
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w',encoding='utf-8')      #在windows系统运行务必设置encoding='utf-8',否则系统会尝试用gbk写然后报错
    f.write("<!- "+SELF_URL_MARKER + page + " -->" + "\n")
    f.write(str(content))
    f.close()

def match_required_url(url,restriction_url):
    return (restriction_url == '*' or restriction_url in url)

count = 0
MAXCOUNT = 50
successful = 0
failed = 0
crawl_only = "https://news.sjtu.edu.cn"

def crawl():
    global successful
    global failed
    global crawl_only
    while True:
        
        page = q.get(block = True,timeout = TIMEOUTSECONDS)
        if not crawled.find(page):
            #print("current page:",page)
            try:
                print("getting:",page)
                content = get_page(page)
            except:
                print(page,"not found or cannot open!")
                failed += 1
                q.task_done()                 #    访问url失败时也要调用queue.task_done()
                continue
            else:
                successful += 1

            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            #print(outlinks)
            global count
            for link in outlinks:
                if (not crawled.find(link)) and count < MAXCOUNT and match_required_url(link,crawl_only):
                    q.put(link)
                    count += 1
            if varLock.acquire():
                graph[page] = outlinks
                crawled.add(page)
                varLock.release()
        print("Tasks left:",q.qsize())
        q.task_done()
        
    
  


if __name__ == '__main__':

   # seed = str(sys.argv[1])
    #method = sys.argv[2]
    #max_page = int(sys.argv[3])

    parser = argparse.ArgumentParser()
    parser.add_argument("-s")
    parser.add_argument("-thread")
    parser.add_argument("-page")
    args = parser.parse_args()

    seed = args.s                   #起始网页url
    THREAD_NUM = int(args.thread)   # 线程数
    MAXCOUNT = int(args.page)       #目标网页数
    
    start_time = time.time()        # 计时器

         
    
    varLock = threading.Lock()
    q = queue.Queue()

    bitset_len = 20 * MAXCOUNT
    crawled = bloomFilter.BloomFilter(bitset_len, bloomFilter.get_optimal_k(bitset_len,MAXCOUNT))
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
    print(f"successful: {successful}, failed: {failed}")
