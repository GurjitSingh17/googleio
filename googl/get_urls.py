from models import vid_link
from models import link as googl_link
from multiprocessing import Pool
import xml.etree.ElementTree as ET
import urllib2
import threading
import time
import requests


def update():
    #pool = Pool(processes=8)
    ids = [video.vid_id for video in vid_link.objects.all()]
    l = len(ids)
    print l
    # parts = []
    # sep = 100
    # for i in range(sep):
    #     x = ((l*i)/sep)
    #     y = ((l*(i+1))/sep)
    #     #print "index", x ,y
    #     parts.append(ids[x:y])
    # #     #print len(new_ids)
    # #     #urls = pool.map(update_googl,new_ids)
    # #     #save_urls(urls)
    threads = [threading.Thread(target=update_googl, args=(id,i,)) for i, id in enumerate(ids)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(10)
    print "===============here=================="
    update_true_urls()
    return


def update_true_urls():
    urls = googl_link.objects.all()
    threads = [threading.Thread(target=update_true, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(10)
    print "===============here=================="
    return


def update_true(url):
    url = url.url
    if googl_link.objects.all().filter(url=url).count() == 0:
        true_url = None
        try:
            true_url = urllib2.urlopen(url).geturl()
        except Exception:
            print "error"
        true_url = true_url if not None else url
        new_url = googl_link(url=url,true_url=true_url)
        new_url.save()
    else:
        old_url = googl_link.objects.all().filter(url=url)[0]
        if not old_url.true_url:
            true_url = None
            try:
                true_url = urllib2.urlopen(url).geturl()
            except Exception:
                print "error"
            true_url = true_url if not None else url
            old_url.true_url = true_url
            old_url.save()

def save_urls(urls):
    for url in urls:
        if url:
            if len(googl_link.objects.all().filter(url=url)) == 0:
                new_url = googl_link(url=url)
                new_url.save()
        # new_url = googl_link(url=url)
        # new_url.save()


def update_googl(id, i):
    base = "https://www.youtube.com/annotations_invideo?features=1&legacy=1&video_id="
    vid_url = base + id
    start = time.time()
    try:
        content = urllib2.urlopen(vid_url).read()
    except Exception:
        return None
    rt = ET.fromstring(content)
    for url in rt.iter("url"):
        goo_url = url.get("value",None)
        if goo_url:
            if goo_url.find("goo.gl") != -1:
                print goo_url
                if googl_link.objects.all().filter(url=goo_url).count() == 0:
                    new_url = googl_link(url=goo_url)
                    new_url.save()

    #print time.time() - start
    return None
    # links = re.findall('"https?://goo.gl/.*?"',content)
    # links = [link.split('"')[1] for link in links if len(link) <= 60]
    # if links:
    #     for link in links:
    #         if len(googl_link.objects.all().filter(url=link)) == 0:
    #             new_url = googl_link(url=link)
    #             new_url.save()
