import os
from PIL import Image

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
targetPath = rootPath + "/assets/kindle.jpeg"

class KindleWidget:
  s_width = 0
  s_height = 0
  s_rotate = True
  left = 0
  top = 0

  def __init__(self, s_width, s_height, s_rotate, left = 0, top = 0) -> None:
    self.s_width = s_width
    self.s_height = s_height
    self.s_rotate = s_rotate
    self.left = left
    self.top = top

  def draw():
    pass

  def render(self, img, w_width, w_height, padLeft, padTop):
    bound = self.__calcBound(img, w_width, w_height, padLeft, padTop)
    self.__drawEips(img, bound[0], bound[1])
    self.__drawImg(img, bound[0], bound[1])

  def __calcBound(self, img, w_width, w_height, padLeft = 0, padTop = 0):
    w_left = self.left + padLeft
    w_top = self.top + padTop
    if(self.s_rotate == True):
      Timage = Image.open(img)
      Timage = Timage.transpose(Image.ROTATE_270)
      Timage.save(img)
      Timage.close()
      w_left = self.s_width - padTop - w_height - self.top
      w_top = self.left + padLeft
    return (w_left, w_top)

  def __drawEips(self, img, x, y):
    # os.system("eips -g " + img + " -x " + str(x) + " -y " + str(y))
    print("eips -g " + img + " -x " + str(x) + " -y " + str(y))

  def __drawImg(self, img, x, y):
    Himage = Image.open(targetPath)
    # Himage = Image.new('1', (1024, 768), 255)
    Himage.paste(Image.open(img), (x, y))
    Himage.save(targetPath)


  def getAlignCenterPos(self, str, font, draw, center, top):
    return (center - draw.textlength(str, font=font) / 2, top)
