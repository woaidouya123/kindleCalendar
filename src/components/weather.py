import os
from PIL import Image,ImageDraw,ImageFont
from kindleWidget import KindleWidget
import requests

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

bgPath = rootPath + "/assets/weather/bg.jpg"
targetPath = rootPath + "/assets/weather/target.jpg"
fontPath = rootPath + "/assets/font.ttf"

class Weather(KindleWidget):
  cityCode = ''
  fontSize = 20
  imgWidth = 44
  font = None
  width = 0
  height = 0
  curWeather = ["-"]*9
  perWeather = ["-"]*9

  def __init__(self, s_width, s_height, s_rotate, left=0, top=0, fontSize = 20, imgWidth = 44, align = "left", cityCode = '101190101', isKindle=False) -> None:
    super().__init__(s_width, s_height, s_rotate, left, top, isKindle)
    self.cityCode = cityCode
    self.fontSize = fontSize
    self.imgWidth = imgWidth
    self.font = ImageFont.truetype(fontPath, fontSize)
    Himage = Image.new('1', (0, 0), 255)
    draw = ImageDraw.Draw(Himage)
    bound = draw.textbbox((0, 0), "大暴雨到特大暴雨", font=self.font)
    self.width = max(bound[2], 44)
    self.height = bound[3]*2 + 44
    Himage = Image.new('1', (self.width, self.height), 255)
    Himage.save(bgPath)

  def getWeatherData(self):
    try:                                                                     # 连接超时,6秒，下载文件超时,7秒
      r = requests.get('http://t.weather.itboy.net/api/weather/city/'+self.cityCode,timeout=(6,7))
      r.encoding = 'utf-8'
      tempList = [
      (r.json()['cityInfo']['city']),             #城市0
      (r.json()['data']['wendu']),                #温度1
      (r.json()['data']['shidu']),                #湿度2
      (r.json()['data']['forecast'][0]['low']),   #今日低温3
      (r.json()['data']['forecast'][0]['high']),  #今日高温4
      (r.json()['data']['forecast'][0]['type']),  #今日天气5
      (r.json()['data']['forecast'][0]['fx']),    #今日风向6
      (r.json()['data']['forecast'][0]['fl']),    #今日风级7
      (r.json()['cityInfo']['updateTime'])        #更新时间8
      ]
    except:
      tempList = ["---"]*9
      return tempList
    else:
      return tempList

  def draw(self, timeNow):
    Himage = Image.open(bgPath)
    draw = ImageDraw.Draw(Himage)
    draw.text((0, 0), "大暴雨到特大暴雨", font=self.font)
    tempTypeIcon = Image.open(rootPath + "/assets/weatherIcon/rainstorm.bmp")
    tempTypeIcon = tempTypeIcon.resize((self.imgWidth, self.imgWidth))
    Himage.paste(tempTypeIcon,(int(self.width / 2 - self.imgWidth / 2), 0))
    self.saveImg(Himage, targetPath)

weather = Weather(1024, 768, True, 512, 234, 20, align="center")
weather.draw(1)

