import os
import datetime
from PIL import Image,ImageDraw,ImageFont
from kindleWidget import KindleWidget

rootPath = os.path.join(os.path.dirname(__file__), "../")

img1Path = rootPath + "/assets/clock/t1.jpg"
img2Path = rootPath + "/assets/clock/t2.jpg"
img3Path = rootPath + "/assets/clock/t3.jpg"
img4Path = rootPath + "/assets/clock/t4.jpg"
timeImages = [img1Path, img2Path, img3Path, img4Path]

bgPath = rootPath + "/assets/clock/bg.jpg"
targetPath = rootPath + "/assets/clock/time.jpg"
fontPath = rootPath + "/assets/font.ttf"

def getAlignCenterPos(str, font, draw, center, top):
  return (center - draw.textlength(str, font=font) / 2, top)

class Clock(KindleWidget):
  left = 0
  top = 0
  fontSize = 20
  border = True
  font = None
  borderWidth = 0
  borderHeight = 0
  width = 0
  height = 0
  startPoints = [0]*4
  curTime = ["-"]*4
  perTime = ["-"]*4

  def __init__(self, left = 0, top = 0, fontSize = 20, border = True) -> None:
    super().__init__()
    self.left = left
    self.top = top
    self.fontSize = fontSize
    self.border = border
    self.font = ImageFont.truetype(fontPath, fontSize)
    Himage = Image.new('1', (1024, 768), 255)
    draw = ImageDraw.Draw(Himage)
    bound = draw.textbbox((0, 0), "8", font=self.font)
    self.borderWidth = int(bound[2] * 1.5)
    self.borderHeight = int(bound[3] * 1.3)
    self.width = self.borderWidth * 5
    self.height = self.borderHeight
    self.startPoints = [1, self.borderWidth, self.borderWidth*3, self.borderWidth*4 - 1]
  
  def draw(self, timeNow):
    print(self.borderWidth, self.borderHeight)
    strtime = timeNow.strftime('%H:%M')
    self.curTime = [strtime[0], strtime[1], strtime[3], strtime[4]]
    Himage = Image.new('1', (self.width, self.height), 255)
    Hdraw = ImageDraw.Draw(Himage)
    Hdraw.text(getAlignCenterPos(":", self.font, Hdraw, self.width / 2, 0), ":", font=self.font)
    for i in range(len(self.curTime)):
      if(self.curTime[i] != self.perTime[i]):
        Timage = Image.new('1', (self.borderWidth, self.borderHeight), 255)
        draw = ImageDraw.Draw(Timage)
        draw.rectangle([0, 0, self.borderWidth - 1, self.borderHeight - 1])
        draw.text(getAlignCenterPos(self.curTime[i], self.font, draw, self.borderWidth / 2, 0), self.curTime[i], font=self.font)
        # Timage = Timage.transpose(Image.ROTATE_270)
        Timage.save(timeImages[i])
        Timage.close
        Himage.paste(Image.open(timeImages[i]), (self.startPoints[i], 0))
    self.perTime = list(self.curTime)
    Himage.save(targetPath)
    Himage.close
    
timeNow = datetime.datetime.now()
test = Clock(100, 200, 100, border=False)
test.draw(timeNow)
