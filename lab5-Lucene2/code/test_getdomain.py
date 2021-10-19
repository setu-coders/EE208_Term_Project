from urllib.parse import urlparse
def get_domain(url):
    return urlparse(url).netloc

if __name__ == '__main__':
    url1 = "https://baike.baidu.com/s/123"
    url2 = "http://jwc.sjtu.edu.cn"
    print(get_domain(url1))
    print(get_domain(url2))