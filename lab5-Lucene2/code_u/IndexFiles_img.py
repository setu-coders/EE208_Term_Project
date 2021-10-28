# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime

# from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
import jieba
import paddle
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
#pip install paddlepaddle,lxml
paddle.enable_static()

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


def get_self_url(content):
    prefix = "<!- SELF_URL_TAG:"
    suffix = " -->"
    off1 = len(prefix)
    off2 = - len(suffix)
    pattern = re.compile(prefix + ".*?" + suffix)
    res = re.search(pattern=pattern,string = content)
    st,ed = res.span()[0],res.span()[1]
    return content[st + off1:ed + off2]

def get_domain(url):
    return urlparse(url).netloc

def get_title(content):
    soup = BeautifulSoup(content,features="html.parser")
    title_ele = soup.find("title")
    title = title_ele.string
    return title
def clean_html(content):
    soup = BeautifulSoup(content,features="html.parser")
    for script in soup(["script", "style"]):   # 去除javascript https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
        script.extract()
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # drop blank lines
    text = '\n'.join(line for line in lines if line)
    return text
def add_imgs(content,pageurl):
    VALID_TEXT_LEN = 20
    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.NONE)  # Not Indexed

    page_title = get_title(content)
    docs = []
    soup = BeautifulSoup(content, features = "html.parser")
    for img_tag in soup.findAll('img'):
        img_url = img_tag.get('src','')
        if len(img_url) < 5:
            continue
        texts = ""
        doc = Document()
        if(img_url[0] == '/'): # is relative link
            img_url = urljoin(pageurl,img_url)
            print(img_url)
        search_prox = list(img_tag.previous_siblings) + list(img_tag.next_siblings) + list(img_tag.parent.next_siblings) + list(img_tag.parent.previous_siblings)
        #全部的文字范围
        for item in search_prox:
            if item.string:
                print(item.string[:20])
                texts += item.string

        if len(texts) < VALID_TEXT_LEN:   # 文字太短或者为空的不要
            continue
        doc.add(Field("title", page_title, t1))
        doc.add(Field("url", pageurl, t1))
        doc.add(Field("img_url", img_url, t1))
        doc.add(TextField("contents",( " ".join(jieba.cut_for_search(texts)) ),Field.Store.YES))
        docs.append(doc)
    return docs

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        # store = SimpleFSDirectory(File(storeDir).toPath())
        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = WhitespaceAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.NONE)  # Not Indexed
        
        t2 = FieldType()
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Indexes documents, frequencies and positions.
        
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.html'):
                    continue
                print("adding", filename)
                DBG = 0
                try:
                    DBG += 1
                    path = os.path.join(root, filename)
                    file = open(path, encoding='utf-8')

                    
                    contents = file.read()
                    #print(contents[:100])
                    page_url = get_self_url(contents)
                    #page_domain = get_domain(page_url)z
                    #page_title = get_title(contents)
                    
                    docs = add_imgs(contents, page_url)
                    print("-"*50)
                    """
                    

                    print(filename,path,page_url,page_domain,page_title)

                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
                    else:
                        print("warning: no content in %s" % filename)
                    """
                    for doc in docs:
                        writer.addDocument(doc)
           
                except Exception as e:
                    print("Failed in indexDocs:", e)
                    

if __name__ == '__main__':
    lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    # import ipdb; ipdb.set_trace()
    start = datetime.now()
    try:
        IndexFiles('../../html_2', "index_img")
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
