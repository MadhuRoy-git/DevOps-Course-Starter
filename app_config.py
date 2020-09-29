import os 

class Config:

    def __init__(self):
        self.KEY = os.getenv('apiKey')
        self.TOKEN = os.getenv('apiToken')
        self.BOARDID = os.getenv('boardId')
    