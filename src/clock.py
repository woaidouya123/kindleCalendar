import datetime
import os
import threading
import time

from PIL import Image,ImageDraw,ImageFont,ImageChops

rootPath = os.path.abspath(os.path.dirname(__file__))
img1Path = rootPath + "/assets/clock/t1.jpg"
img2Path = rootPath + "/assets/clock/t2.jpg"
img3Path = rootPath + "/assets/clock/t3.jpg"
img4Path = rootPath + "/assets/clock/t4.jpg"
bgPath = rootPath + "/assets/clock/bg.jpg"
targetPath = rootPath + "/assets/clock/time.jpg"

fontPath = rootPath + "/assets/font.ttf"
fontSize = ImageFont.truetype(fontPath, 200)
borderWidth = 150
borderHeight = 250
topOffset = 259
middleLine = 512
startPoints = [162, 312, 562, 712]
curTime = ["-"]*4
perTime = ["-"]*4
timeImages = [img1Path, img2Path, img3Path, img4Path]

def getAlignCenterPos(str, font, draw, center, top):
  return (center - draw.textsize(str, font=font)[0] / 2, top)

# 初始化背景
def initBg():
  Himage = Image.new('1', (1024, 768), 255)
  draw = ImageDraw.Draw(Himage)
  for point in startPoints:
    draw.rectangle([point, topOffset, point + borderWidth, topOffset + borderHeight])
  draw.text(getAlignCenterPos(":", fontSize, draw, middleLine, topOffset), ":", font=fontSize)
  Himage = Himage.transpose(Image.ROTATE_270)
  Himage.save(bgPath)
  Himage.close()
  os.system("eips -g " + bgPath)
  print("eips -g " + bgPath)

# 更新时间（全局）
def updateTimeFull():
  Himage = Image.open(bgPath)
  for i in range(len(startPoints)):
    Timage = Image.open(timeImages[i])
    Himage.paste(Timage,(topOffset + 1, startPoints[i] + 1))
  Himage.save(targetPath)
  Himage.close()

# 更新页面（局部）
def updateTimePortial():
  global perTime
  for i in range(len(curTime)):
    if(curTime[i] != perTime[i]):
      os.system("eips -g " + timeImages[i] + " -x " + str(topOffset + 1) + " -y " + str(startPoints[i] + 1))
      print("eips -g " + timeImages[i] + " -x " + str(topOffset + 1) + " -y " + str(startPoints[i] + 1))
  perTime = list(curTime)

# 绘制时间
def drawTime(timeNow):
  global curTime
  strtime = timeNow.strftime('%H:%M')
  curTime = [strtime[0], strtime[1], strtime[3], strtime[4]]
  for i in range(len(curTime)):
    Timage = Image.new('1', (borderWidth - 2, borderHeight - 2), 255)
    draw = ImageDraw.Draw(Timage)
    draw.text(getAlignCenterPos(curTime[i], fontSize, draw, 75, 0), curTime[i], font=fontSize)
    Timage = Timage.transpose(Image.ROTATE_270)
    Timage.save(timeImages[i])
    Timage.close
  updateTimePortial()
  # updateTimeFull()

clearCount = 0 # 重置屏幕时间

# 绘制
def draw():
  global perTime
  global clearCount
  while(True):
    clearCount = clearCount - 1
    if (clearCount <= 0):
      os.system("eips -c")
      initBg()
      perTime = ["-"]*4
      clearCount = 10
    timeNow = datetime.datetime.now()
    drawTime(timeNow)
    delta = float(str(timeNow.second) + "." + str(timeNow.microsecond))
    time.sleep(60 - delta)

time.sleep(3)
timeThreading = threading.Thread(target=draw, args=())
timeThreading.start()