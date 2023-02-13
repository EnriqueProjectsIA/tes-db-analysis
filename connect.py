import pymongo
import datetime

class DatabaseTes:

    def __init__(self,local:bool):
        self.local = local
        self.db = False

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
            client = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS = MONGO_TIMEOUT)
            self.db =client.CSIC


        except pymongo.errors.ServerSelectionTimeoutError as TimeOutExceed:
            print('Timeout exceeded')
        except pymongo.errors.ConnectionFailure as errorConnection:
            print('Connection failure ')+errorConnection
    
    def collection(self,collection:str):

        assert self.db != False, 'Se necesita el método connect'
        assert collection in ['tes'], 'La collección no existe'

        if collection == 'tes':
            self.collec = self.db.tes


if __name__ == '__main__':
    objeto = DatabaseTes(True)
    objeto.connect()
    db = objeto.collection('tes')