#-*- coding:utf-8 -*-
import requests
import json

APIKEY = '626b7a4f416a48454771576241464467474330705a496e2f54646a6535514c69625164745a6338664a442f'

path = '/home/yuinityk/OneDrive/workspace/ShiritoriAI/output.wav'
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)

files = {"a": open(path, 'rb'), "v": "on"}
r = requests.post(url, files=files)
print r.json()['text']
print r.json()['message']
print r.json().values()
print r.json().keys()
