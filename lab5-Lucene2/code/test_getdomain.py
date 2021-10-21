from urllib.parse import urlparse
def get_domain(url):
    return urlparse(url).netloc

def get_rooturl(url):
    return url[:url.find('//')] + "//" + get_domain(url)
if __name__ == '__main__':
    url1 = "https://baike.baidu.com/s/123"
    url2 = "https://news.sjtu.edu.cn/fafs/sadsd"
    print(get_rooturl(url1))
    print(get_rooturl(url2))