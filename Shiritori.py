#-*- coding:utf-8 -*-
import MeCab

mecab = MeCab.Tagger('-Ochasen')
mecab.parse('')
node = mecab.parseToNode('強連結成分分解')
while node:
    print(node.surface, node.feature)
    node = node.next
