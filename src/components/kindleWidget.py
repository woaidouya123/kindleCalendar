import os
import math
from PIL import Image, ImageChops

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
targetPath = rootPath + "/assets/kindle.jpeg"
bgPath = rootPath + "/assets/bg.png"

class KindleWidget:
  s_width = 0
  s_height = 0
  s_rotate = True
  left = 0
  top = 0
  isKindle = False

  def __init__(self, s_width, s_height, s_rotate, left = 0, top = 0, isKindle = False) -> None:
    self.s_width = s_width
    self.s_height = s_height
    self.s_rotate = s_rotate
    self.left = left
    self.top = top
    self.isKindle = isKindle

  def draw():
    pass

  def render(self, img, w_width, w_height, padLeft, padTop):
    bound = self.__calcBound(w_width, w_height, padLeft, padTop)
    if(self.isKindle == True):
      self.__drawEips(img, bound[0], bound[1])
    self.__drawImg(img, bound[0], bound[1])

  def __calcBound(self, w_width, w_height, padLeft = 0, padTop = 0):
    w_left = self.left + padLeft
    w_top = self.top + padTop
    if(self.s_rotate == True):
      w_left = self.s_height - padTop - w_height - self.top
      w_top = self.left + padLeft
    return (w_left, w_top)

  def __drawEips(self, img, x, y):
    os.system("eips -g " + img + " -x " + str(x) + " -y " + str(y))
    print("eips -g " + img + " -x " + str(x) + " -y " + str(y))

  def __drawImg(self, img, x, y):
    Himage = Image.open(targetPath)
    Himage.paste(Image.open(img), (x, y))
    Himage.save(targetPath)
    Himage.close()

  def saveBgImg(self, Himage, path, x, y):
    Bimage = ImageChops.invert(Image.open(bgPath).crop((x, y, x + Himage.width, y + Himage.height)))
    Himage = ImageChops.invert(Himage)
    Himage = ImageChops.invert(ImageChops.add(Bimage, Himage, 1, 0))
    Himage.save(path)
    Himage.close()

  def saveImg(self, Himage, path):
    if(self.s_rotate == True):
      Himage = Himage.transpose(Image.ROTATE_270)
    Himage.save(path)
    Himage.close()

  # 计算字体居中显示时文字起始坐标
  def getAlignCenterPos(self, str, font, draw, center, top):
    return (center - draw.textlength(str, font=font) / 2, top)

  # 计算点xy绕center旋转angle角度后的坐标
  def getRotatePos(self, xy: tuple, center: tuple, angle: float):
    return [
      (xy[0] - center[0]) * math.cos(angle) - (xy[1] - center[1]) * math.sin(angle) + center[0],
      (xy[0] - center[0]) * math.sin(angle) + (xy[1] - center[1]) * math.cos(angle) + center[1],
    ]
