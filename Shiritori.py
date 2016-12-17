#-*- coding:utf-8 -*-
import MeCab
import random
import copy
import sys

accept = ['名詞-一般']
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
    f.close()
    return wdic

def get_endletter(w):
    va = ['ア','ァ','カ','サ','タ','ナ','ハ','マ','ヤ','ャ','ラ','ワ','ガ','ザ','ダ','バ','パ']
    vi = ['イ','ィ','キ','シ','チ','ニ','ヒ','ミ',          'リ',     'ギ','ジ','ヂ','ビ','ピ']
    vu = ['ウ','ゥ','ク','ス','ツ','ヌ','フ','ム','ユ','ュ','ル',     'グ','ズ','ヅ','ブ','プ','ヴ']
    ve = ['エ','ェ','ケ','セ','テ','ネ','ヘ','メ',          'レ',     'ゲ','ゼ','デ','ベ','ペ']
    vo = ['オ','ォ','コ','ソ','ト','ノ','ホ','モ','ヨ','ョ','ロ','ヲ','ゴ','ゾ','ド','ボ','ポ']
    yoon = ['ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ']

    if w.rstrip('、。')[-1] == 'ー':
        endletter = mecab.parse(w.rstrip('ー、。')).split('\t')[-5][-1]
        if endletter in va:
            return 'ア'
        elif endletter in vi:
            return 'イ'
        elif endletter in vu:
            return 'ウ'
        elif endletter in ve:
            return 'エ'
        elif endletter in vo:
            return 'オ'
        else:
            f = open('error.log','a')
            f.write('get_endletter error(-): ' + endletter + '\n')
            f.close()

    endletter = mecab.parse(w.rstrip('ー、。')).split('\t')[-5][-1]
    if endletter in yoon:
        return mecab.parse(w.rstrip('ー、。')).split('\t')[-5][-2:]
    elif endletter in va or endletter in vi or endletter in vu or endletter in ve or endletter in vo:
        return mecab.parse(w.rstrip('ー、。')).split('\t')[-5][-1]
    else:
        f = open('error.log','a')
        f.write('get_endletter error(parse): ' + endletter + '\n')
        f.close()

def return_word(el,wdic): #el='チ'など
    return random.choice(wdic[el])

def learn_word(words,savedic): #wdicにない単語をsaveに入れる
    wdic = load_dic()
    save = copy.deepcopy(savedic)
    parsed = mecab.parse(words.rstrip('、。')).split('\t')
    for i in range(len(parsed)):
        if parsed[i] in accept:
            if len(parsed[i-2]) == len([ch for ch in parsed[i-2] if "ア" <= ch <= "ン"]):
                if parsed[i-2] not in wdic[parsed[i-2][:1]]:
                    if parsed[i-2][:1] in save.keys():
                        save[parsed[i-2][:1]].append(parsed[i-2])
                    else:
                        save[parsed[i-2][:1]] = [parsed[i-2]]
    return save

def dict_update(wdic,add):
    for key in add.keys():
        wdic[key].extend(add[key])

def save_dic(add,mode='a'):
    f = open('dic.csv',mode)
    keys = list(add.keys())
    keys.sort()
    for key in keys:
        for word in add[key]:
            f.write(key + ',' + word + '\n')
    f.close()

def play(mode='endless'):
    wdic = load_dic()
    while 1:
        print('you:',end='')
        w = input()
        if w == 'exit':
            exit()
        else:
            el = get_endletter(w)
            if len(wdic[el]) == 0:
                print('I lose!')
                savedic = learn_word(w,{})
                save_dic(savedic)
                exit()
            else:
                re = return_word(el,wdic)
                print('me:'+re)
                savedic = learn_word(w,{})
                save_dic(savedic)
                if mode != 'endless':
                    wdic[el].remove(re)

if __name__ == '__main__':
    print('Which mode?(endless,vs)> ',end='')
    mode = input()
    play(mode)
