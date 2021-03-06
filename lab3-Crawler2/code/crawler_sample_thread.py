# SJTU EE208

import threading
import queue
import time


def get_page(page):
    print('downloading page %s' % page)
    time.sleep(0.5)
    return g.get(page, [])


def get_all_links(content):
    return content


def working():
    while True:
        print("getting","left:",q.qsize())
        page = q.get()
        # if varLock.acquire():
        if page not in crawled:
            # varLock.release()
            # else:
            # varLock.release()
            content = get_page(page)
            outlinks = get_all_links(content)
            for link in outlinks:
                q.put(link)
            if varLock.acquire():
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
            print(q.qsize())
            q.task_done()


g = {'A': ['B', 'C', 'D'],
     'B': ['E', 'F'],
     'C': ['1', '2'],
     '1': ['3', '4'],
     'D': ['G', 'H'],
     'E': ['I', 'J'],
     'G': ['K', 'L'],
     }

start = time.time()
NUM = 4
crawled = []
graph = {}
varLock = threading.Lock()
q = queue.Queue()
q.put('A')
for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    t.start()
q.join()
end = time.time()
print(end - start)
