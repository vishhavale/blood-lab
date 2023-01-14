class dbSSO:
    userName,password="",""    
    def __init__(self,userName=None,Password=None):
        self.userName = userName
        self.password = Password
    def chkSSO(self):
        if self.userName is not None and self.password is not None:
            
            #chck in db
            return True
        return False
    def register(self):   
        pass

#def registerSso(data):
