import datetime
import os
import threading
import time

from PIL import Image,ImageDraw,ImageFont,ImageChops

rootPath = os.path.abspath(os.path.dirname(__file__))
imgPath = rootPath.replace("\\","/") + "/assets/kindle.jpeg"
fontPath = rootPath + "/assets/font.ttf"

fontSize16 = ImageFont.truetype(fontPath, 16)
fontSize20 = ImageFont.truetype(fontPath, 20)
fontSize25 = ImageFont.truetype(fontPath, 25)
fontSize30 = ImageFont.truetype(fontPath, 30)
fontSize60 = ImageFont.truetype(fontPath, 60)
fontSize70 = ImageFont.truetype(fontPath, 70)

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


def DrawHorizontalDar(draw,timeUpdate):
  strtime = timeUpdate.strftime('%Y-%m-%d') #年月日
  strtime2 = timeUpdate.strftime('%H:%M')   #时间
  strtimeW = timeUpdate.strftime('%w') #星期
  #显示星期
  draw.text((44, 30), TodayWeek(strtimeW), font = fontSize30, fill = 0)
  #显示时间   
  draw.text((180,20 ), strtime2, font = fontSize60, fill = 0)
  #显示年月日
  draw.text((44, 70), strtime, font = fontSize20, fill = 0)

# timeNow = datetime.datetime.now()
# draw = ImageDraw.Draw(Himage)
# DrawHorizontalDar(draw, timeNow)
# Himage.save(imgPath)

def draw():
  while(True):
    Himage = Image.new('1', (1024, 768), 255)
    timeNow = datetime.datetime.now()
    delta = float(str(timeNow.second) + "." + str(timeNow.microsecond))
    draw = ImageDraw.Draw(Himage)
    DrawHorizontalDar(draw, timeNow)
    Himage.save(imgPath)
    os.system("eips -c")
    os.system("eips -g " + imgPath)
    print(delta)
    time.sleep(60 - delta)

timeThreading = threading.Thread(target=draw, args=())
timeThreading.start()