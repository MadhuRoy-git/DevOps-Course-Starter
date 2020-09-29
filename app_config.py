import os 

class Config:

    def __init__(self):
        self.key = os.getenv('apiKey')
        self.token = os.getenv('apiToken')
        self.boardid = os.getenv('boardId')
    