#-*- coding:utf-8 -*-
import feedparser
import MeCab

accept = ['名詞-一般']

def load_dic():
    wdic = {}
    f = open('dic.csv','r')
    for line in f:
        t,w = line.split(",")
        w = w.rstrip()
        if t in wdic.keys():
            wdic[t].append(w)
        else:
            wdic[t] = [w]
    f.close()
    return wdic

def save_dic(add,mode='a'):
    f = open('dic.csv',mode)
    keys = list(add.keys())
    keys.sort()
    for key in keys:
        for word in add[key]:
            f.write(key + ',' + word + '\n')
    f.close()

wdic = load_dic()
add = {}

mecab = MeCab.Tagger('-Ochasen')
RSS = ["http://rss.dailynews.yahoo.co.jp/fc/rss.xml","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=ir","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=y","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=w","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=b","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=p","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=e","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=s","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=t","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=po"]
for rss in RSS:
    news_dic = feedparser.parse(rss)
    
    for entry in news_dic.entries:
        title = entry.title
        parsed = mecab.parse(title).split('\t')
        print(parsed)
        for i in range(len(parsed)):
            if parsed[i].rstrip()[:2] == '名詞':
                if parsed[i] in accept:
                    if len(parsed[i-2]) == len([ch for ch in parsed[i-2] if "ア" <= ch <= "ン"]):
                        if parsed[i-2] not in wdic[parsed[i-2][:1]]:
                            if parsed[i-2][:1] in add.keys():
                                add[parsed[i-2][:1]].append(parsed[i-2])
                            else:
                                add[parsed[i-2][:1]] = [parsed[i-2]]
    
        wdic.update(add)
        save_dic(wdic,'w')
