import os
import time
import datetime
from PIL import Image
from components import numClock

rootPath = os.path.abspath(os.path.dirname(__file__))
targetPath = rootPath + "/assets/kindle.jpeg"

def clearImg():
  Himage = Image.new('1', (1024, 768), 255)
  Himage.save(targetPath)
  Himage.close()

def clearEips():
  os.system("eips -c")

clearImg()
clock1 = numClock.NumClock(1024, 768, True, 512, 200, 100, False, "center")
def draw():
  while True:
    timeNow = datetime.datetime.now()
    delta = float(str(timeNow.second) + "." + str(timeNow.microsecond))
    clock1.draw(timeNow)
    time.sleep(60 - delta)

draw()






