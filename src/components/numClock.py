import os
from PIL import Image,ImageDraw,ImageFont
from kindleWidget import KindleWidget

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

img1Path = rootPath + "/assets/clock/t1.jpg"
img2Path = rootPath + "/assets/clock/t2.jpg"
img3Path = rootPath + "/assets/clock/t3.jpg"
img4Path = rootPath + "/assets/clock/t4.jpg"
timeImages = [img1Path, img2Path, img3Path, img4Path]

bgPath = rootPath + "/assets/clock/bg.jpg"
fontPath = rootPath + "/assets/font.ttf"

class NumClock(KindleWidget):
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

  def __init__(self, s_width, s_height, s_rotate, left = 0, top = 0, fontSize = 20, border = True, align = "left", isKindle = False) -> None:
    super().__init__(s_width, s_height, s_rotate, left, top, isKindle)
    self.fontSize = fontSize
    self.border = border
    self.font = ImageFont.truetype(fontPath, fontSize)
    Himage = Image.new('1', (100, 100), 255)
    draw = ImageDraw.Draw(Himage)
    bound = draw.textbbox((0, 0), "8", font=self.font)
    self.borderWidth = int(bound[2] * 1.5)
    self.borderHeight = int(bound[3] * 1.3)
    self.width = self.borderWidth * 5
    self.height = self.borderHeight
    # 对齐方式
    if(align == "center"):
      self.left = self.left - int(self.width / 2)
    elif(align == "right"):
      self.left = self.left - self.width
    self.startPoints = [1, self.borderWidth, self.borderWidth*3, self.borderWidth*4 - 1]
    Himage = Image.new('1', (self.width, self.height), 255)
    Hdraw = ImageDraw.Draw(Himage)
    Hdraw.text(self.getAlignCenterPos(":", self.font, Hdraw, self.width / 2, 0), ":", font=self.font)
    Himage.save(bgPath)
    Himage.close()
    self.render(bgPath, self.width, self.height, 0, 0)

  def reset(self):
    self.perTime = ["-"]*4
    self.render(bgPath, self.width, self.height, 0, 0)

  def draw(self, timeNow):
    print(self.borderWidth, self.borderHeight)
    strtime = timeNow.strftime('%H:%M')
    self.curTime = [strtime[0], strtime[1], strtime[3], strtime[4]]
    for i in range(len(self.curTime)):
      if(self.curTime[i] != self.perTime[i]):
        Timage = Image.new('1', (self.borderWidth, self.borderHeight), 255)
        draw = ImageDraw.Draw(Timage)
        if(self.border == True):
          draw.rectangle([0, 0, self.borderWidth - 1, self.borderHeight - 1])
        draw.text(self.getAlignCenterPos(self.curTime[i], self.font, draw, self.borderWidth / 2, 0), self.curTime[i], font=self.font)
        Timage.save(timeImages[i])
        Timage.close()
        self.render(timeImages[i], self.borderWidth, self.borderHeight, self.startPoints[i], 0)
    self.perTime = list(self.curTime)

# timeNow = datetime.datetime.now()
# test = NumClock(1024, 768, False, 400, 400, fontSize=80, align='right',border=False)
# test.draw(timeNow)
