# SJTU EE208
# -*-coding:utf-8-*-
import os
import math
import re
import string
import sys
from typing import final
import urllib
import requests
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
from fake_useragent import UserAgent
#from selenium import webdriver
#import selenium_test

TIMEOUTSECONDS = 5 #访问超时时间
MAXFILENAMELENGTH = 50  #文件名最长不超过的长度
SELF_URL_MARKER  = "SELF_URL_TAG:"   # 爬取到的网页写入文件时，在html文件末尾附上该网页的url方便查询
ua = UserAgent()
header = {
        'User-Agent': ua.random,
        'Referer': 'https://www.gog.com/zh/game/cyberpunk_2077',
        'Cookie': "gog_lc=CN_CNY_zh-Hans; _gcl_au=1.1.1023331159.1638773721; _ga=GA1.2.765414947.1638773721; cat_ab=old; csrf=true; cart_token=426eb3e696e3da04; gog_wantsmaturecontent=18"
        }

#chrome_options = webdriver.ChromeOptions()
#refs = {"profile.managed_default_content_settings.images": 2}
#chrome_options.add_experimental_option("prefs", prefs)
#browser = webdriver.Chrome(chrome_options=chrome_options)
#browser = webdriver.Chrome()
def valid_filename(s):
    valid_chars = "-_(). %s%s" % (string.ascii_letters, string.digits)  
    s = ''.join((c if c != '.' else '+') for c in s if c in valid_chars)    # 去掉文件名.
    return s[:MAXFILENAMELENGTH] + '.html'    # 防止文件名过长


def get_page(page,coding = 'utf-8'):
    global successful
    global failed
    try:
        #request = Request(page, headers=header)
        #content = urlopen(request,timeout = TIMEOUTSECONDS).read()
        r = requests.get(page, allow_redirects=True)
        content = r.content
        #print("crawling",page)
        #browser = webdriver.Chrome()
        #browser.get(page)
        #content = browser.page_source
        #browser.close()
    except Exception as E:
        
        print(E)
        #raise ValueError
    else:
        return content.decode(coding)

def get_all_links2(content, pageurl):
    links = []
    soup = BeautifulSoup(content, features="html.parser")
    for url in re.findall(r"\"url\":\"(.*?),", content):
        url = url[7:-1]
        #print(url)
        if '/zh/' not in url:
           url = '/zh/game' + url
        if url[:4] != "http":
           url = urllib.parse.urljoin(pageurl,url) 
        
        #print(url)
        links.append(url)

    return links

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
    folder = 'html_gog' 
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

def match_required_url(url,restriction_urls):
    if not restriction_urls:
        return True
    for restr in restriction_urls:
        if restr in url:
            return True
    return False

def switch2zh(url):
    return url.replace("/en/", "/zh/")

count = 0
MAXCOUNT = 50
successful = 0
failed = 0
crawl_only = ["https://www.gog.com/en/game","https://www.gog.com/zh/game","https://www.gog.com/game/"]
save_only = "https://www.gog.com/zh/game/"
MAXDEPTH = 1
def crawl():
    global successful
    global failed
    global crawl_only
    while True:
        
        page, curDepth = q.get(block = True,timeout = TIMEOUTSECONDS)
        if not crawled.find(page):
            #print("current page:",page)
            try:
                page = switch2zh(page)
                print("getting:",page)
                content = get_page(page)
            except:
                print(page,"not found or cannot open!")
                failed += 1
                q.task_done()                 #    访问url失败时也要调用queue.task_done()
                continue
            else:
                successful += 1
            if match_required_url(page, save_only):
                add_page_to_folder(page, content)
            outlinks = get_all_links2(content, page)
            #print(outlinks)
            #print(outlinks)
            global count
            for link in outlinks:
                if (not crawled.find(link)) and count < MAXCOUNT and match_required_url(link,crawl_only) and curDepth < MAXDEPTH:
                    q.put((link, curDepth + 1))
                    count += 1
            if varLock.acquire():
                #graph[page] = outlinks
                crawled.add(page)
                varLock.release()
        print("Tasks left:",q.qsize())
        q.task_done()
        
    
  


if __name__ == '__main__':

   # seed = str(sys.argv[1])
    #method = sys.argv[2]
    #max_page = int(sys.argv[3])

    parser = argparse.ArgumentParser()
    #parser.add_argument("-s")
    parser.add_argument("-thread")
    parser.add_argument("-page")
    args = parser.parse_args()

    #seed = args.s   
    #起始网页url
    seeds = [f"https://www.gog.com/games?sort=title&page={i}" for i in range(1, 145)]
    THREAD_NUM = int(args.thread)   # 线程数
    MAXCOUNT = int(args.page)       #目标网页数
    
    start_time = time.time()        # 计时器

         
    
    varLock = threading.Lock()
    q = queue.Queue()

    bitset_len = 20 * MAXCOUNT
    crawled = bloomFilter.BloomFilter(bitset_len, bloomFilter.get_optimal_k(bitset_len,MAXCOUNT))
    #graph = {}

    for seed in seeds:
        q.put((seed, 0))
    
    for i in range(THREAD_NUM):
        t = threading.Thread(target=crawl)
        t.daemon = True
        t.start()
    
    print("Start Working!")
    q.join()            # 等待queue为空
    
    
    
    end_time = time.time()
    print(f"total time used:{(end_time - start_time)}")
    print(f"successful: {successful}, failed: {failed}")
    #browser.close()