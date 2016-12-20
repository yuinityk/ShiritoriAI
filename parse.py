#-*- coding:utf-8 -*-
import feedparser
import MeCab
from Shiritori import *

wdic = load_dic('hard')

mecab = MeCab.Tagger('-Ochasen')
RSS = ["http://rss.dailynews.yahoo.co.jp/fc/rss.xml","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=ir","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=y","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=w","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=b","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=p","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=e","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=s","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=t","http://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&topic=po","http://www3.nhk.or.jp/rss/news/cat0.xml","http://www3.nhk.or.jp/rss/news/cat1.xml","http://www3.nhk.or.jp/rss/news/cat2.xml","http://www3.nhk.or.jp/rss/news/cat3.xml","http://www3.nhk.or.jp/rss/news/cat4.xml","http://www3.nhk.or.jp/rss/news/cat5.xml","http://www3.nhk.or.jp/rss/news/cat6.xml","http://www3.nhk.or.jp/rss/news/cat7.xml"]
for rss in RSS:
    news_dic = feedparser.parse(rss)
    
    for entry in news_dic.entries:
        title = entry.title
        add = learn_word(title,{}) 
        dict_update(wdic,add)
        save_dic(wdic,'w')
