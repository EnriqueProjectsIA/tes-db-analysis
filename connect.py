import pymongo
import datetime

class DatabaseTes:

    def __init__(self,local:bool):
        self.local = local

    def connect(self):
        if self.local == True:
            MONGO_HOST = 'localhost'
            MONGO_PORT = '27017'
            MONGO_URI = 'mongodb://'+MONGO_HOST+':'+MONGO_PORT+'/'
        elif self.local == False:
            with open('secrets.txt', 'r') as handle:
                user,pass_ = [i.strip().split(':')[1] for i in handle.readlines()]
            MONGO_URI = f'mongodb+srv://{user}:{pass_}@cisccluster0.8yysq.mongodb.net/test'
            
        
        MONGO_TIMEOUT = 1000
            
        
        try:
            self.client = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS = MONGO_TIMEOUT)
        except pymongo.errors.ServerSelectionTimeoutError as TimeOutExceed:
            print('Timeout exceeded')
        except pymongo.errors.ConnectionFailure as errorConnection:
            print('Connection failure ')+errorConnection
        

if __name__ == '__main__':
    print('ok')