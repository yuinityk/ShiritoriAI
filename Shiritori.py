#-*- coding:utf-8 -*-
import MeCab
import random
import sys

mecab = MeCab.Tagger('-Ochasen')
mecab.parse('')
'''
node = mecab.parseToNode('強連結成分分解')

while node:
    print(node.surface, node.feature)
    node = node.next
'''


def load_dic():
    wdic = {}
    f = open('dic.csv','r')
    for line in f:
        t,w = line.split(",")
        w = w.rstrip()
        if t in wdic.keys():
            wdic[t].append(w)
        else:
            wdic[t]=[w]

    return wdic

def get_endletter(w):
    return mecab.parse(w.rstrip('、。')).split('\t')[-5][-1]

def return_word(el): #el='チ'など
    wdic=load_dic()
    return random.choice(wdic[el])
    
if __name__ == '__main__':
    w = sys.argv[1]
    print(return_word(get_endletter(w)))
