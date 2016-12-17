#-*- coding:utf-8 -*-
import requests
import json
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

APIKEY = '626b7a4f416a48454771576241464467474330705a496e2f54646a6535514c69625164745a6338664a442f'

path = '/home/yuinityk/OneDrive/workspace/ShiritoriAI/output.wav'
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)

p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = CHUNK)
print("* recording")
frames = []

for i in range(0,int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

files = {"a": open(path, 'rb'), "v": "on"}
r = requests.post(url, files=files)
print(r.json()['text'])
print(r.json()['message'])
print(r.json().values())
print(r.json().keys())
