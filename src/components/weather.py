import os
from PIL import Image,ImageDraw,ImageFont
from kindleWidget import KindleWidget
import requests

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

bgPath = rootPath + "/assets/weather/bg.jpg"
targetPath = rootPath + "/assets/weather/target.jpg"
fontPath = rootPath + "/assets/font.ttf"

WeatherIconDict = {
  '大雨': 'heavyRain.bmp',
  '中到大雨': 'heavyRain.bmp',
  '暴雨': 'rainstorm.bmp',
  '大暴雨': 'rainstorm.bmp',
  '特大暴雨': 'rainstorm.bmp',
  '大到暴雨': 'rainstorm.bmp',
  '暴雨到大暴雨': 'rainstorm.bmp',
  '大暴雨到特大暴雨': 'rainstorm.bmp',
  '沙尘暴': 'sandstorm.bmp',
  '浮尘': 'sandstorm.bmp',
  '扬沙': 'sandstorm.bmp',
  '强沙尘暴': 'sandstorm.bmp',
  '雾霾': 'sandstorm.bmp',
  '晴': 'sunny.bmp',
  '阴': 'cloudy.bmp',
  '多云': 'partlyCloudy.bmp',
  '小雨': 'lightRain.bmp',
  '中雨': 'moderateRain.bmp',
  '阵雨': 'shower.bmp',
  '雷阵雨': 'thunderShower.bmp',
  '小到中雨': 'lightModerateRain.bmp',
  '雷阵雨伴有冰雹': 'thunderShowerHail.bmp',
  '雾': 'fog.bmp',
  '冻雨': 'sleet.bmp',
  '雨夹雪': 'rainSnow.bmp',
  '阵雪': 'snowShower.bmp',
}

class Weather(KindleWidget):
  cityCode = ''
  fontSize = 20
  imgWidth = 44
  font = None
  bigFont = None
  width = 0
  height = 0
  curWeather = ["-"]*8
  perWeather = [" "]*8

  def __init__(self, s_width, s_height, s_rotate, left=0, top=0, width = 200, height = 100, align = "left", fontSize = 20, imgWidth = 44, cityCode = '101190101', isKindle=False) -> None:
    super().__init__(s_width, s_height, s_rotate, left, top, isKindle)
    self.cityCode = cityCode
    self.fontSize = fontSize
    self.imgWidth = imgWidth
    self.font = ImageFont.truetype(fontPath, fontSize)
    self.bigFont = ImageFont.truetype(fontPath, int(fontSize * 1.5))
    self.width = width
    self.height = height
    if(align == "center"):
      self.left = self.left - int(self.width / 2)
    elif(align == "right"):
      self.left = self.left - self.width
    Himage = Image.new('1', (0, 0), 255)
    Himage = Image.new('1', (self.width, self.height), 255)
    Himage.save(bgPath)

  def getWeatherData(self):
    try:                                                                     # 连接超时,6秒，下载文件超时,7秒
      r = requests.get('http://t.weather.itboy.net/api/weather/city/'+str(self.cityCode),timeout=(6,7))
      r.encoding = 'utf-8'
      tempList = [
      (r.json()['cityInfo']['city']),             #城市0
      (r.json()['data']['wendu'] + '℃'),                #温度1
      (r.json()['data']['shidu']),                #湿度2
      (r.json()['data']['forecast'][0]['low'] + '-' + r.json()['data']['forecast'][0]['high']),   #今日低温-高温3
      (r.json()['data']['forecast'][0]['type']),  #今日天气4
      (r.json()['data']['forecast'][0]['fx']),    #今日风向5
      (r.json()['data']['forecast'][0]['fl']),    #今日风级6
      (r.json()['cityInfo']['updateTime'])        #更新时间7
      ]
    except:
      tempList = ["-"]*8
      return tempList
    else:
      return tempList

  def draw(self, timeNow):
    if(self.curWeather == ["-"]*8 or timeNow.hour >= 7 and timeNow.hour < 22 and timeNow.minute == 0):
      self.curWeather = self.getWeatherData()
      needRefresh = False
      for i in range(len(self.curWeather)):
        if(self.curWeather[i] != self.perWeather[i]):
          needRefresh = True
          break
      if(needRefresh):
        Himage = Image.open(bgPath)
        draw = ImageDraw.Draw(Himage)
        draw.text(self.getAlignCenterPos(self.curWeather[4], self.font, draw, self.width / 2, self.imgWidth), self.curWeather[4], font=self.font)
        draw.text(self.getAlignCenterPos(self.curWeather[3], self.font, draw, self.width / 2, self.imgWidth + self.fontSize * 1.3), self.curWeather[3], font=self.font)
        draw.text(self.getAlignCenterPos(self.curWeather[1], self.bigFont, draw, (self.width / 2 - self.imgWidth / 2) / 2, 0), self.curWeather[1], font=self.bigFont)
        draw.text(self.getAlignCenterPos(self.curWeather[2], self.bigFont, draw, (self.width / 2 + self.imgWidth / 2) + (self.width / 2 - self.imgWidth / 2) / 2, 0), self.curWeather[2], font=self.bigFont)
        tempTypeIcon = Image.open(rootPath + "/assets/weatherIcon/" +WeatherIconDict.get(self.curWeather[4], 'noWeatherType.bmp'))
        tempTypeIcon = tempTypeIcon.resize((self.imgWidth, self.imgWidth))
        Himage.paste(tempTypeIcon,(int(self.width / 2 - self.imgWidth / 2), 0))
        self.saveImg(Himage, targetPath)
        self.render(targetPath, self.width, self.height, 0, 0)
      self.perWeather = list(self.curWeather)
