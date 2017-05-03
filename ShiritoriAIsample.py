#-*- coding:utf-8 -*-
import requests
import json
import pyaudio
import wave
import subprocess

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

APIKEY = '6e4a37754e6b425465433566567a643155382e4a6148425152747678616f7330593975534d616b57354136'

#path = '/home/yuinityk/OneDrive/workspace/ShiritoriAI/output.wav'
path = 'output.wav'
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

subprocess.call("sox output.wav -r 16000 put.wav",shell=True)
subprocess.call("sox put.wav output.wav gain -n",shell=True)

files = {"a": open(path, 'rb'), "v": "on"}
r = requests.post(url, files=files)
print(r.json())
print(r.json()['text'])
print(r.json()['results'][0]['tokens'][len(r.json()['results'][0]['tokens'])-2]['spoken'])
print(r.json().values())
print(r.json().keys())
