#-*- coding:utf-8 -*-
import MeCab
import random
import copy
import sys
import pyaudio
import wave
import requests

accept = ['名詞-一般']
va = ['ア','ァ','カ','サ','タ','ナ','ハ','マ','ヤ','ャ','ラ','ワ','ガ','ザ','ダ','バ','パ']
vi = ['イ','ィ','キ','シ','チ','ニ','ヒ','ミ',          'リ',     'ギ','ジ','ヂ','ビ','ピ']
vu = ['ウ','ゥ','ク','ス','ツ','ヌ','フ','ム','ユ','ュ','ル',     'グ','ズ','ヅ','ブ','プ','ヴ']
ve = ['エ','ェ','ケ','セ','テ','ネ','ヘ','メ',          'レ',     'ゲ','ゼ','デ','ベ','ペ']
vo = ['オ','ォ','コ','ソ','ト','ノ','ホ','モ','ヨ','ョ','ロ','ヲ','ゴ','ゾ','ド','ボ','ポ']
yoon = ['ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ']

#wave const
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

APIKEY = '626b7a4f416a48454771576241464467474330705a496e2f54646a6535514c69625164745a6338664a442f'
path = '/home/yuinityk/OneDrive/workspace/ShiritoriAI/output.wav'
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)

mecab = MeCab.Tagger('-Ochasen')
mecab.parse('')

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = CHUNK)
    frames = []
    print("* recording...")
    for i in range(0,int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate
    print("* done recording.")

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def word_recognize():
    files = {"a": open(path, 'rb'), "v": "on"}
    r = requests.post(url, files=files)
    return r.json()['results'][0]['tokens'][len(r.json()['results'][0]['tokens'])-2]['spoken']

def load_dic(diff):
    wdic = {}
    f = open('dic_' + diff + '.csv','r')
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
    if w.rstrip('、。0123456789')[-1] == 'ー':
        endletter = mecab.parse(w.rstrip('ー、。0123456789')).split('\t')[-5][-1]
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

    endletter = mecab.parse(w.rstrip('ー、。0123456789')).split('\t')[-5][-1]
    if endletter in yoon:
        return mecab.parse(w.rstrip('ー、。0123456789')).split('\t')[-5][-2:]
    elif endletter in va or endletter in vi or endletter in vu or endletter in ve or endletter in vo:
        return mecab.parse(w.rstrip('ー、。0123456789')).split('\t')[-5][-1]
    else:
        f = open('error.log','a')
        f.write('get_endletter error(parse): ' + endletter + '\n')
        f.close()

def return_word(el,wdic):
    return random.choice(wdic[el])

def learn_word(words,savedic): #wdicにない単語をsaveに入れて返す
    wdic = load_dic('hard')
    save = copy.deepcopy(savedic)
    parsed = mecab.parse(words.rstrip('、。')).split('\t')
    for i in range(len(parsed)):
        if parsed[i] in accept:
            if len(parsed[i-2]) == len([ch for ch in parsed[i-2] if "ア" <= ch <= "ン"]):
                if len(parsed[i-2]) > 1 and parsed[i-2][1] in yoon:
                        if parsed[i-2] not in wdic[parsed[i-2][:2]]:
                            if parsed[i-2][:2] in save.keys():
                                save[parsed[i-2][:2]].append(parsed[i-2])
                            else:
                                save[parsed[i-2][:2]] = [parsed[i-2]]
                elif parsed[i-2] not in wdic[parsed[i-2][:1]]:
                    if parsed[i-2][:1] in save.keys():
                        save[parsed[i-2][:1]].append(parsed[i-2])
                    else:
                        save[parsed[i-2][:1]] = [parsed[i-2]]
    return save

def dict_update(wdic,add):
    for key in add.keys():
        wdic[key].extend(add[key])

def save_dic(add,mode='a'):
    f = open('dic_hard.csv',mode)
    keys = list(add.keys())
    keys.sort()
    for key in keys:
        for word in add[key]:
            f.write(key + ',' + word + '\n')
    f.close()

def play(mode = 'endless', diff = 'easy'):
    wdic = load_dic(diff)
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

def play_record(mode = 'endless', diff = 'easy'):
    wdic = load_dic(diff)
    while 1:
        print('press any key to record')
        _ = input()
        record()
        w = word_recognize()
        print('you:'+w.rstrip('、。'))
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
    print('Choose difficulty:easy,normal,hard.> ',end='')
    while(1):
        diff = input()
        if diff in ['easy','normal','hard']:
            break
        print('Input any one word of "easy", "normal" and "hard".')
    play_record(mode,diff)
