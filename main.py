import time
import requests
from queue import Queue
from threading import Thread
import threading
import os

for i in range(1, 11):
    if os.path.isfile("sites/sites_{}.txt".format(i)):
        os.remove("sites/sites_{}.txt".format(i))
    else:
        continue


lock = threading.Lock()


size = 0


siteCount = 0
count = 1
save = "sites/sites_{}.txt"


def download_site(save, urls):
    global size
    global siteCount
    global count
    global lock
    while not urls.empty():
        try:
            x = requests.get(urls.get(block=False))
        except requests.exceptions.RequestException as e:
            print(e)
            lock.acquire()
            siteCount += 1
            lock.release()
            urls.task_done()
            continue

        lock.acquire()
        siteCount += 1
        print("\n downloaded site", siteCount, x.url)
        urls.task_done
        with open(save.format(count), "a", encoding="utf-8") as f:
            f.write(x.text)
        
        if siteCount % 10 == 0:
            size += os.path.getsize(save.format(count))
            count += 1
            print("\n count:", count)
        lock.release()


urls = Queue()
with open("urls.txt", "rt") as f1:
    for line in f1:
        urls.put(line.strip())
print("sites count:", urls.qsize())


threads = []
N = 12
start = time.time()
for i in range(N):
    t = Thread(target=download_site, args=(save, urls))
    t.setDaemon(True)
    threads.append(t)
    t.start()


for t in threads:
    t.join()
    print("\n", t.name, "has joined")
end = time.time()
TotalTime = end-start
print("time taken: {:.4f}".format(TotalTime), "seconds")
size += os.path.getsize(filename=save.format(count))
rate = size/TotalTime
print("{:.2f}".format(rate), "Bytes per second")

