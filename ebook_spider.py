#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import threading
import os
import codecs

url = 'http://www.00ksw.net/html/13/13835/'
pagelist = {}
threads_num = 100
page = {}

def sub(_s, _start, _end):
    try:
        sidx = _s.index(_start)
        eidx = _s.index(_end, sidx)
        return _s[sidx:eidx]
    except Exception, e:
        #print e
        pass
        
    return u""
        

def get_page_list():
    page = {}
    try:
        r = requests.get(url)
        r.encoding = 'gbk'
        content = sub(r.text, u'<div id="list">', u'</div>')
        m = re.findall(u'<dd><a href="([^"]+)">([^<]+)</a>', content)
        if len(m) > 0:
            for i in range(len(m)):
                page[i] = m[i]
    except Exception, e:
        print(e)
        
    return page

def down_pages(start, end):
    global page
    
    if end > start:
        for i in range(end - start):
            if pagelist.has_key(start + i):
                page_url = url + pagelist[start + i][0]
                try:
                    while True:
                        r = requests.get(page_url)
                        r.encoding = 'gbk'
                        content = sub(r.text, u'<div id="content">', u'</div>')
                        if len(content) > 0:
                            content = re.sub(u'<br[^>]*>', u'\n', content)
                            content = re.sub(u'<[^>]+>', u'', content)
                            content = re.sub(u'&nbsp', u'', content)
                            content = re.sub(u';;;;', u'', content)
                            
                            page[start + i] = content
                            print u"download: %s \t %s" % (pagelist[start+i][1], pagelist[start+i][0])
                            break
                        else:
                            print u"try again: %s \t %s" % (pagelist[start+i][1], pagelist[start+i][0])
                except Exception, e:
                    print e
                


if __name__ == '__main__':
    pagelist = get_page_list()
    count = len(pagelist)
    
    threads = []
    
    # 获取页面列表后，多线程下载
    for i in range(threads_num):
        start = (count / threads_num) * i
        end = (count / threads_num) * (i + 1)
        t = threading.Thread(target=down_pages, args=(start, end))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    f = codecs.open('择天记.txt', 'wt', encoding='utf-8')
        
    # 写文件
    for i in range(len(pagelist.keys())):
        if page.has_key(i):
            
            title = re.sub(u'第.*章', u'', pagelist[i][1])
            if i > 0:
                f.write(u"\n\n第%d章 %s" % (i, title))
            else:
                f.write(title)
            f.write(u'\n\n');
            f.write(page[i])
        else:
            print "skip key:%d %s\n" % (i, pagelist[i][1])
    f.close()
        
    
    