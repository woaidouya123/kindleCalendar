from todoist_api_python.api import TodoistAPI

api = TodoistAPI('ae9258d9e28828f5a12ae2071e69adbe7a6a8e12')

try:
    tasks = api.get_tasks(filter="1 days")
    for task in tasks:
      print(task.content)
except Exception as error:
    print(error)