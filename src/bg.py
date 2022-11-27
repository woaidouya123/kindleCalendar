import random
import os
import requests
import json
from PIL import Image
targetPath = os.path.abspath(os.path.dirname(__file__)) + '/assets/bg.png'

URL = "https://www.duitang.com/napi/blog/list/by_filter_id/?filter_id=壁纸_电脑壁纸&start=0&limit=100"

def getImage():
  response = requests.get(URL)
  img_list = json.loads(response.content.decode('utf-8'))["data"]["object_list"]
  selected = random.randint(0, len(img_list) - 1)
  return img_list[selected]["photo"]["path"]

def saveImage(url):
  r = requests.get(url)
  with open(targetPath, 'wb') as f:
    f.write(r.content)

def processImage(path):
  Himage = Image.open(path)
  Himage = Himage.convert('L')
  print(Himage.width, Himage.height, 999)
  w_scale = 1024 / Himage.width
  h_scale = 768 / Himage.height
  if(w_scale > h_scale):
    Himage = Himage.resize((1024, int(Himage.height * w_scale)))
  else:
    Himage = Himage.resize((int(Himage.width * h_scale), 768))
  Himage = Himage.transpose(Image.ROTATE_270)
  Himage = Himage.crop((0, 0, 768, 1024))
  Himage.save(path)

url = getImage()
saveImage(url)
processImage(targetPath)
