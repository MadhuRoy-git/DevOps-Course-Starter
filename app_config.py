import os 

class Config:

    def __init__(self):
        self.key = os.getenv('key')
        self.token = os.getenv('token')
        self.boardid = os.getenv('boardid')
    