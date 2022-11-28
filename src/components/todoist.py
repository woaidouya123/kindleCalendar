import os
from PIL import Image,ImageDraw,ImageFont
from kindleWidget import KindleWidget
from todoist_api_python.api import TodoistAPI

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

bgPath = rootPath + "/assets/todoist/bg.jpg"
emptyPath = rootPath + "/assets/todoist/empty.png"
targetPath = rootPath + "/assets/todoist/target.jpg"
fontPath = rootPath + "/assets/font.ttf"

class TodoList(KindleWidget):
  fontSize = 20
  lineHeight = 24
  api = None
  border = True
  font = None
  width = 0
  height = 0
  curTodo = []
  perTodo = []

  def __init__(self, s_width, s_height, s_rotate, left = 0, top = 0, width = 200, height = 80, align = "left", fontSize = 20, border = True, authCode = "0123456789", isKindle = False) -> None:
    super().__init__(s_width, s_height, s_rotate, left, top, isKindle)
    self.width = width
    self.height = height
    self.border = border
    self.fontSize = fontSize
    self.api = TodoistAPI(authCode)
    self.font = ImageFont.truetype(fontPath, fontSize)
    Himage = Image.new('1', (self.width, self.height), 255)
    draw = ImageDraw.Draw(Himage)
    bound = draw.textbbox((0, 0), "米", font=self.font)
    self.lineHeight = bound[3] + bound[1]
    self.maxLength = self.width // (bound[2])
    # 对齐方式
    if(align == "center"):
      self.left = self.left - int(self.width / 2)
    elif(align == "right"):
      self.left = self.left - self.width
    if(self.border == True):
      draw.rectangle([1, 1, self.width - 1, self.height - 1])
    self.saveBgImg(Himage, bgPath, self.left, self.top)
    self.perTodo = [{'title': '-'}]

  def getTodoList(self):
    try:
      tasks = self.api.get_tasks(filter="today")
      return tasks
    except Exception as error:
      print(error)
      return []

  def reset(self):
    self.curTodo = []
    self.perTodo = [{'title': '-'}]

  def draw(self, timeNow):
    if(len(self.curTodo) != len(self.perTodo) or timeNow.minute % 5 == 0):
      tasks = self.getTodoList()
      self.curTodo = []
      for task in tasks:
        title = '○' + task.content
        if(len(title) > self.maxLength):
          title = title[:self.maxLength - 1] + "..."
        self.curTodo.append({
          'title': title,
          'desc': task.description,
          "date": task.due.string
        })
      needRefresh = False
      if(len(self.curTodo) != len(self.perTodo)):
        needRefresh = True
      if(not needRefresh):
        for i in range(len(self.curTodo)):
          if(self.curTodo[i]['title'] != self.perTodo[i]['title'] or self.curTodo[i]['desc'] != self.perTodo[i]['desc'] or self.curTodo[i]['date'] != self.perTodo[i]['date']):
            needRefresh = True
            break
      if(needRefresh):
        Himage = Image.open(bgPath)
        draw = ImageDraw.Draw(Himage)
        for i in range(len(self.curTodo)):
          draw.text((0, self.lineHeight * i), self.curTodo[i]['title'], font=self.font)
        if(len(self.curTodo) == 0):
          emptyImage = Image.open(emptyPath)
          Himage.paste(emptyImage, (int(self.width / 2) - 17, int(self.height / 2) - 16), 0)
        self.saveImg(Himage, targetPath)
        self.render(targetPath, self.width, self.height, 0, 0)
        self.perTodo = list(self.curTodo)
