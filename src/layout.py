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
  configMap[k] = int(v)

def clearImg():
  Himage = Image.new('1', (configMap["width"], configMap["height"]), 255)
  if(configMap["rotate"] == 1):
    Himage = Himage.transpose(Image.ROTATE_270)
  Himage.save(targetPath)
  Himage.close()

def clearEips():
  os.system("eips -c")
  print("eips -c")

def clear():
  clearImg()
  if(configMap["mode"] == 1):
    clearEips()

def draw():
  clearCount = 0 # 重置屏幕时间
  clear()
  clock1 = NumClock(configMap["width"], configMap["height"], configMap["rotate"] == 1, 512, 400, 200, True, "center", isKindle=configMap["mode"] == 1)
  clock2 = TickClock(configMap["width"], configMap["height"], configMap["rotate"] == 1, 512, 50, 300, True, "center", isKindle=configMap["mode"] == 1)
  while True:
    clearCount = clearCount - 1
    if (clearCount <= 0):
      clear()
      clock1.reset()
      clearCount = 10
    timeNow = datetime.datetime.now()
    delta = float(str(timeNow.second) + "." + str(timeNow.microsecond))
    clock1.draw(timeNow)
    clock2.draw(timeNow)
    time.sleep(60 - delta)

draw()

# time.sleep(3)
# timeThreading = threading.Thread(target=draw, args=())
# timeThreading.start()






