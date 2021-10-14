import re
def get_self_url(content):
    prefix = "<!- SELF_URL_TAG:"
    suffix = " -->"
    off1 = len(prefix)
    off2 = - len(suffix)
    pattern = re.compile(prefix + ".*?" + suffix)
    res = re.search(pattern=pattern,string = content)
    st,ed = res.span()[0],res.span()[1]
    return content[st + off1:ed + off2]



def get_title(content):
    prefix = "<title>"
    suffix = "</title>"
    off1 = len(prefix)
    off2 = - len(suffix)
    pattern = re.compile(prefix + ".*?" + suffix)
    res = re.search(pattern=pattern,string = content)
    st,ed = res.span()[0],res.span()[1]
    return content[st + off1:ed + off2]

s = "grafjssjd <!- SELF_URL_TAG:http://image.baidu.sjtu.edu.com.cn.wtf --> fassaf<!DOCTYPE html>  <meta property=\"qc:admins\" content=\"465267610762567726375\" ><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" ><title>Python 正则表达式 | 菜鸟教程</title>"


print(get_self_url(s))
print(get_title(s))