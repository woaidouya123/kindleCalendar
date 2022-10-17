import datetime
import os
import threading
import time
import requests
from configparser import ConfigParser

from PIL import Image,ImageDraw,ImageFont,ImageChops

rootPath = os.path.abspath(os.path.dirname(__file__))
imgPath = rootPath.replace("\\","/") + "/assets/kindle.jpeg"
fontPath = rootPath + "/assets/font.ttf"
cfg = ConfigParser()
cfg.read(rootPath + "/config.ini",encoding="utf-8")
config = cfg.items("KindleCalendar")

fontSize16 = ImageFont.truetype(fontPath, 16)
fontSize20 = ImageFont.truetype(fontPath, 20)
fontSize25 = ImageFont.truetype(fontPath, 25)
fontSize30 = ImageFont.truetype(fontPath, 30)
fontSize40 = ImageFont.truetype(fontPath, 40)
fontSize60 = ImageFont.truetype(fontPath, 60)
fontSize70 = ImageFont.truetype(fontPath, 70)
fontSize200 = ImageFont.truetype(fontPath, 200)

#居中显示的方法 一个字宽度30像素 例如重479像素开始 多加一个字 少空 15 个像素
def AlignCenter(string,scale,startPixel):
  charsCount = 0
  for s in string:
    charsCount += 1
  charsCount *= scale/2
  charsCount = startPixel - charsCount
  return charsCount

#获取天气
def GetTemp():
  try:                                                                     # 连接超时,6秒，下载文件超时,7秒
    r = requests.get('http://t.weather.itboy.net/api/weather/city/'+config[0][1],timeout=(6,7)) 
    r.encoding = 'utf-8'
    tempList = [
    (r.json()['cityInfo']['city']),             #城市0
    (r.json()['data']['shidu']),                #湿度1
    (r.json()['data']['forecast'][0]['low']),   #今日低温2
    (r.json()['data']['forecast'][0]['high']),  #今日高温3
    (r.json()['data']['forecast'][0]['type']),  #今日天气4
    (r.json()['data']['forecast'][0]['fx']),    #今日风向5
    (r.json()['data']['forecast'][0]['fl']),    #今日风级6
    (r.json()['cityInfo']['updateTime'])        #更新时间22
    ]
  except:
    tempList = ["---"]*8
    return tempList
  else:
    return tempList

weatherData = GetTemp()

#匹配天气类型图标
def UpdateWeatherIcon(tempType):
  if(tempType == "大雨"  or tempType == "中到大雨"):
    return "heavyRain.bmp"
  elif(tempType == "暴雨"  or tempType == "大暴雨" or 
    tempType == "特大暴雨" or tempType == "大到暴雨" or
    tempType == "暴雨到大暴雨" or tempType == "大暴雨到特大暴雨"):
    return "rainstorm.bmp"
  elif(tempType == "沙尘暴" or tempType == "浮尘" or
    tempType == "扬沙" or tempType == "强沙尘暴" or
    tempType == "雾霾"):
    return "sandstorm.bmp"
  elif(tempType == "晴"):
    return "sunny.bmp"
  elif(tempType == "阴"):
    return "cloudy.bmp"
  elif(tempType == "多云"):
    return "partlyCloudy.bmp"
  elif(tempType == "小雨"):
    return "lightRain.bmp"
  elif(tempType == "中雨"):
    return "moderateRain.bmp"
  elif(tempType == "阵雨"):
    return "shower.bmp"
  elif(tempType == "雷阵雨"):
    return "thunderShower.bmp"
  elif(tempType == "小到中雨"):
    return "lightModerateRain.bmp"
  elif(tempType == "雷阵雨伴有冰雹"):
    return "thunderShowerHail.bmp"
  elif(tempType == "雾"):
    return "fog.bmp"
  elif(tempType == "冻雨"):
    return "sleet.bmp"
  elif(tempType == "雨夹雪"):
    return "rainSnow.bmp"
  elif(tempType == "阵雪"):
    return "snowShower.bmp"
  return "noWeatherType.bmp"

def TodayWeek(nowWeek):
  if nowWeek == "0":
    return"星期天"
  elif nowWeek =="1":
    return"星期一"
  elif nowWeek =="2":
    return"星期二"
  elif nowWeek =="3":
    return"星期三"
  elif nowWeek =="4":
    return"星期四"
  elif nowWeek =="5":
    return"星期五"
  elif nowWeek =="6":
    return"星期六"

# bmp = Image.open(rootPath + '/assets/bg.png')
# Himage.paste(bmp,(0,0))
# Himage = Himage.transpose(Image.ROTATE_90)


def DrawTime(draw, timeUpdate):
  strtime = timeUpdate.strftime('%Y-%m-%d') #年月日
  strtime2 = timeUpdate.strftime('%H:%M')   #时间
  strtimeW = timeUpdate.strftime('%w') #星期
  #显示星期
  draw.text((44, 90), TodayWeek(strtimeW), font = fontSize60, fill = 0)
  #显示时间
  # print(draw.textsize(strtime2, font = fontSize200))
  draw.text((512 - draw.textsize(strtime2, font = fontSize200)[0] / 2, 20), strtime2, font = fontSize200, fill = 0)
  #显示年月日
  draw.text((44, 170), strtime, font = fontSize40, fill = 0)

def DrawWeather(draw, Himage):
  tempTypeIcon = Image.open(rootPath + "/assets/weatherIcon/" + UpdateWeatherIcon(weatherData[4]))
  tempTypeIcon = tempTypeIcon.resize((66, 66))
  Himage.paste(tempTypeIcon,(840, 90))
  draw.text((873 - draw.textsize(weatherData[4], font = fontSize25)[0] / 2, 155), weatherData[4], font = fontSize25, fill = 0)
  temp = weatherData[2] + "-" + weatherData[3]
  draw.text((873 - draw.textsize(temp, font = fontSize20)[0] / 2, 190), temp, font = fontSize20, fill = 0)

# Himage = Image.new('1', (1024, 768), 255)
# timeNow = datetime.datetime.now()
# draw = ImageDraw.Draw(Himage)
# DrawTime(draw, timeNow)
# DrawWeather(draw)
# Himage.save(imgPath)

def draw():
  while(True):
    Himage = Image.new('1', (1024, 768), 255)
    timeNow = datetime.datetime.now()
    delta = float(str(timeNow.second) + "." + str(timeNow.microsecond))
    draw = ImageDraw.Draw(Himage)
    DrawTime(draw, timeNow)
    DrawWeather(draw, Himage)
    Himage = Himage.transpose(Image.ROTATE_270)
    Himage.save(imgPath)
    os.system("eips -c")
    os.system("eips -g " + imgPath)
    print(delta)
    time.sleep(60 - delta)

def drawWeather():
  while(True):
    weatherData = GetTemp()
    print(weatherData)
    time.sleep(3600)

timeThreading = threading.Thread(target=draw, args=())
weatherThreading = threading.Thread(target=drawWeather, args=())
timeThreading.start()
weatherThreading.start()
