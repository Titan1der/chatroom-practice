class Chatroom:
    
    def __init__(self):
        self.users = [{}]
        self.chatLog = []
        
    def get_chatlog(self):
        return self.chatLog