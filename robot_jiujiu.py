#coding=utf-8
from aip import AipSpeech
import pyaudio
import speech_recognition as sr
import requests
import json
from playsound import playsound


APP_ID='17144783'
API_KEY='ADD_YOUR_KEY'
SECRET_KEY='ADD_YOURKEY'
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

tuling_key='7d14fa4bc295404a9fced576c37453e5'
url='http://api.ruyi.ai/v1/message?q='
add_url='&app_key=ADD_YOUR_KEY&user_id=ADD_YOUR_ID'
headers={'Content-Type': 'application/json;charset=UTF-8'}

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def recog():
        say=sr.Recognizer()
        with sr.Microphone(sample_rate=16000) as source:
                print('-------请讲话--------------')
                audio=say.listen(source)
        with open("audio.wav","wb") as f:
                f.write(audio.get_wav_data())

def listen():
    try:
        result=client.asr(get_file_content('audio.wav'), 'wav', 16000, {'dev_pid': 1537})
        say_text=result['result'][0]
        print('我:'+say_text)
        return say_text
    except:
        print("待机状态.........")

def ai_bot(text):
        if "白了个白" in text or "拜了个拜" in text:
            exit()
#            print("啾啾:拜了个拜")
#            return "拜了个拜"
        try:
                ask=requests.get(url=url+text+add_url)
                ai_ask=json.loads(ask.text)["result"]["intents"][0]["outputs"][0]["property"]["text"].replace('\\n','')
                print("啾啾:"+ai_ask)
                return ai_ask
        except:
            print("Bruse:啊我报错啦，赶紧找我的爸爸修一下")
            return "啊我报错啦，赶紧找我的爸爸修一下"

def make_voice(text):
    result  = client.synthesis(text, 'zh', 1, {
    'spd': 4,
    'vol': 5,
    'per': 4,
    })

    if not isinstance(result, dict):
        with open('ask.mp3', 'wb') as f:
            f.write(result)

def play():
    playsound('ask.mp3')
def main():
    while True:
        recog()
        make_voice(ai_bot(listen()))
        play()

if __name__=="__main__":
    main()
