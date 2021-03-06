#-*- encoding:utf-8 -*-
import sys, os, threading, time
from datetime import datetime

# from java.io import File

#import jieba
#import paddle
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_self_url(content):
    prefix = "<!- SELF_URL_TAG:"
    suffix = " -->"
    off1 = len(prefix)
    off2 = - len(suffix)
    pattern = re.compile(prefix + ".*?" + suffix)
    res = re.search(pattern=pattern,string = content)
    st,ed = res.span()[0],res.span()[1]
    return content[st + off1:ed + off2]

def get_domain(url): # 返回域名
    return urlparse(url).netloc

def get_title(soup): # 返回游戏标题
    #soup = BeautifulSoup(content,features="html.parser")
    title_tag = soup.find("meta",{"property":"og:title"})
    title = title_tag.get("content",'')#.string
    return title

def get_price(soup):  # 返回游戏价格
    tag_feat = "product-actions-price__final-amount _price ng-binding"
    tag_price = soup.find('span',{"class":tag_feat})
    return tag_price.string

def get_description(soup): # 返回游戏简介
    desc_tag = soup.find("meta",{"property":"og:description"})
    desc = desc_tag.get("content",'')#.string
    return desc.strip()

def get_genre(soup): # 返回一个list，其中第0个元素是游戏category，后面的是tag。
    res = []
    catg_tag = soup.find("a",{"href":re.compile("games\?category=(...)")})
    genre_href = catg_tag.get("href",'')
    genre_name = catg_tag.string
    res.append((genre_href, genre_name))
    for sib in catg_tag.find_next_siblings():
        genre_href = sib.get("href",'')
        genre_name = sib.string
        res.append((genre_href, genre_name))
        
    return res

def test(root):
        """
        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.NONE)  # Not Indexed
        
        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Indexes documents, frequencies and positions.
        """
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.html'):
                    continue
                print("adding", filename)
                TT = 1
                while TT > 0:
                    TT -= 1
                    path = os.path.join(root, filename)
                    file = open(path, encoding='utf-8')

                    contents = file.read()
                    soup = BeautifulSoup(contents,features="html.parser")
                    #print(contents[:100])
                    page_url = get_self_url(contents)
                    page_domain = get_domain(page_url)
                    game_title = get_title(soup)
                    game_description = get_description(soup)
                    game_price = get_price(soup)
                    game_genre = get_genre(soup)
                    #contents = clean_html(contents)
                    
                    #cut_words = jieba.cut_for_search(contents)    # requires paddlepaddle. -> pip install paddlepaddle
                    #contents = " ".join(cut_words)
                    #print(contents)
                    file.close()
                    
                    """
                    doc = Document()
                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", path, t1))
                    doc.add(Field("url", page_url, t1))
                    doc.add(TextField("site",page_domain,Field.Store.YES))       # 不能用t1，要想搜索site必须把site设为indexed！
                    doc.add(Field("title", page_title, t1))
                    """

                    print('\n'.join([filename,path,page_url,page_domain,game_title,game_description,game_price]))
                    print(game_genre)
                    """
                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
                    else:
                        print("warning: no content in %s" % filename)
                    writer.addDocument(doc)
                    """
                #except Exception as e:
                 #   print("Failed in indexDocs:", e)


if __name__ == '__main__':
    test('gog_html')