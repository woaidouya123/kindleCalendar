import os
import time
import datetime
import threading
from PIL import Image
from components import *
from configparser import ConfigParser

rootPath = os.path.abspath(os.path.dirname(__file__))
targetPath = rootPath + "/assets/kindle.jpeg"
cfg = ConfigParser()
cfg.read(rootPath + "/config.ini",encoding="utf-8")
config = cfg.items("KindleCalendar")
configMap = {}
for k,v in config:
  print(k,v)
  configMap[k] = v

def clearImg():
  Himage = Image.new('1', (int(configMap["width"]), int(configMap["height"])), 255)
  if(configMap["rotate"] == '1'):
    Himage = Himage.transpose(Image.ROTATE_270)
  Himage.save(targetPath)
  Himage.close()

def clearEips():
  os.system("eips -c")
  print("eips -c")

def clear():
  clearImg()
  if(configMap["mode"] == '1'):
    clearEips()

def draw():
  clearCount = 0 # 重置屏幕时间
  clear()
  numClock = NumClock(int(configMap["width"]), int(configMap["height"]), configMap["rotate"] == '1', 512, 400, 200, True, "center", isKindle=configMap["mode"] == '1')
  tickClock = TickClock(int(configMap["width"]), int(configMap["height"]), configMap["rotate"] == '1', 512, 50, 300, True, "center", isKindle=configMap["mode"] == '1')
  weather = Weather(int(configMap["width"]), int(configMap["height"]), configMap["rotate"] == '1', 50, 130, 300, 150, "left", fontSize=30, imgWidth=66, cityCode=configMap["citycode"], isKindle=configMap["mode"] == '1')
  todoList = TodoList(int(configMap["width"]), int(configMap["height"]), configMap["rotate"] == '1', 974, 130, 300, 225, "right", fontSize=26, border=False, authCode=configMap["authcode"], isKindle=configMap["mode"] == '1')
  while True:
    clearCount = clearCount - 1
    if (clearCount <= 0):
      clear()
      numClock.reset()
      weather.reset()
      todoList.reset()
      clearCount = 10
    timeNow = datetime.datetime.now()
    delta = float(str(timeNow.second) + "." + str(timeNow.microsecond))
    numClock.draw(timeNow)
    tickClock.draw(timeNow)
    weather.draw(timeNow)
    todoList.draw(timeNow)
    time.sleep(60 - delta)

draw()

# time.sleep(3)
# timeThreading = threading.Thread(target=draw, args=())
# timeThreading.start()






