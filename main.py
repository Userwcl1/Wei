from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY'] #敏敏
cityw = os.environ['CITYW'] #我
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_w=os.environ["USER_W"] #我
user_id = os.environ["USER_ID"] #敏敏
template_id = os.environ["TEMPLATE_ID"]

#敏敏的天气

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])


#我的天气

def get_weatherw():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + cityw
  resw = requests.get(url).json()
  weatherw = resw['data']['list'][0]
  return weatherw['weather'], math.floor(weatherw['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_wordsw():
  wordsw = requests.get("https://api.shadiao.pro/chp")
  if wordsw.status_code != 200:
    return get_wordsw()
  return wordsw.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
weaw,temperaturew = get_weatherw()
data = {"city":{"value":city},"weather":{"value":wea},"temperature":{"value":temperature},
      "love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}} #敏敏
dataw = {"cityw":{"value":cityw},"weatherw":{"value":weaw},"temperaturew":{"value":temperaturew},"wordsw":{"value":get_wordsw(), "color":get_random_color()}} #我
res = wm.send_template(user_id,template_id, data) #敏敏
resw = wm.send_template(user_w,template_id, dataw) #我
print(res,resw)
print(resw,res)

