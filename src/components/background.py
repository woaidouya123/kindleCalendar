import os
from PIL import Image
from kindleWidget import KindleWidget

imgPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/background/"))

class Background(KindleWidget):
  def __init__(self, s_width, s_height, s_rotate, left=0, top=0, isKindle=False) -> None:
    super().__init__(s_width, s_height, s_rotate, left, top, isKindle)


