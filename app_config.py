import os 

class Config:

    def __init__(self):
        self.KEY = os.getenv('apiKey')
        self.TOKEN = os.getenv('apiToken')
        self.BOARDID = os.getenv('boardId')
        self.TODOLISTID = os.getenv('TODO_LIST_ID')
        self.DOINGLISTID = os.getenv('DOING_LIST_ID')
        self.DONELISTID = os.getenv('DONE_LIST_ID')
    