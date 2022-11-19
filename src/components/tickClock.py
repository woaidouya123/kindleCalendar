import datetime
import os
import math
from PIL import Image,ImageDraw
from kindleWidget import KindleWidget

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

bgPath = rootPath + "/assets/tick/bg.jpg"
targetPath = rootPath + "/assets/tick/target.jpg"

class TickClock(KindleWidget):
  width = 200

  def __init__(self, s_width, s_height, s_rotate, left = 0, top = 0, width = 20, border = True, align = "left", isKindle = False) -> None:
    super().__init__(s_width, s_height, s_rotate, left, top, isKindle)
    self.width = width
    self.align = align
    self.border = border
    if(align == "center"):
      self.left = self.left - int(self.width / 2)
    elif(align == "right"):
      self.left = self.left - self.width
    self.borderWidth = max(self.width // 40, 1)
    self.tickLen = max(int(self.width / 2 / 6), 3)
    self.subTickLen = int(self.tickLen / 3 * 2)
    self.tickWidth = self.borderWidth
    self.subTickWidth = max(int(self.tickWidth / 3 * 2), 1)
    self.drawBg()

  def drawBg(self):
    Himage = Image.new("1", (self.width, self.width), 255)
    draw = ImageDraw.Draw(Himage)
    # 表盘边框
    if(self.border == True):
      draw.arc([0, 0, self.width, self.width], 0, 360, fill=0, width=self.borderWidth)
    # 表盘刻度
    for i in range(12):
      angle = math.pi * 2 / 12 * i
      start = self.getRotatePos((self.width/2, self.subTickLen), (self.width/2, self.width/2), angle)
      end = self.getRotatePos((self.width/2, 0), (self.width/2, self.width/2), angle)
      draw.line(start + end, fill=0, width=self.subTickWidth)
    for i in range(4):
      angle = math.pi * 2 / 4 * i
      start = self.getRotatePos((self.width/2, self.tickLen), (self.width/2, self.width/2), angle)
      end = self.getRotatePos((self.width/2, 0), (self.width/2, self.width/2), angle)
      draw.line(start + end, fill=0, width=self.tickWidth)
    Himage.save(bgPath)
    Himage.close()

  def draw(self, timeNow):
    Himage = Image.open(bgPath)
    draw = ImageDraw.Draw(Himage)

    # 表盘指针
    minuteAngle = timeNow.minute * (math.pi * 2 / 60)
    hourAngle = (timeNow.hour % 12) * (math.pi * 2 / 12) + minuteAngle / (math.pi * 2) * (math.pi * 2 / 12)

    hourStart = self.getRotatePos((self.width/2, self.tickLen * 4), (self.width/2, self.width/2), hourAngle)
    hourEnd = self.getRotatePos((self.width/2, self.width/2 + self.subTickLen), (self.width/2, self.width/2), hourAngle)
    draw.line(hourStart + hourEnd, fill=0, width=self.tickWidth)

    minuteStart = self.getRotatePos((self.width/2, self.tickLen * 2), (self.width/2, self.width/2), minuteAngle)
    minuteEnd = self.getRotatePos((self.width/2, self.width/2 + self.subTickLen), (self.width/2, self.width/2), minuteAngle)
    draw.line(minuteStart + minuteEnd, fill=0, width=self.subTickWidth)
    self.saveImg(Himage, targetPath)
    self.render(targetPath, self.width, self.width, 0, 0)

# timeNow = datetime.datetime.now()
# test = TickClock(1024, 768, True, 512, 234, width=300, align="center", border=False)
# test.draw(timeNow)
