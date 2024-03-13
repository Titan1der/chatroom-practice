class ServerEnv():
    def __init__(self):
        self.JOIN = {}
        self.WATCH = {}
        self.ROOMS = {
            "1" : "AAAA",
            "2" : "BBBB",
            "3" : "CCCC",
            }
        
    def get_join_list(self):
        return self.JOIN
    
    def get_watch_list(self):
        return self.WATCH
    
    def get_rooms_list(self):
        return self.ROOMS