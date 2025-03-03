import os
import psycopg2
from psycopg2.extras import RealDictCursor


from abc import abstractmethod

class iDatabase:
    
    @abstractmethod
    def connect(self, connection_config, connector_config):...
    
    @abstractmethod
    def connection(self): ...

    @abstractmethod
    def close(self):...



class Database(iDatabase):
    def __init__(self, connection_config, connector_config):
        self.conn = None
        self.connection_config = connection_config
        self.connector_config = connector_config

    def connect(self):
        
        connection_method = self.connector_config.get("connection_method")
        
        try:
            self.conn = connection_method(**self.connection_config)
        except Exception as e:
            raise e
    
    @property    
    def connection(self):
        if self.conn is None:
            self.connect()
        return self.conn
    
    def close(self):
        if self.conn:
            close_f = self.connector_config.get("close_method") # close_f = "close"
        
            if type(close_f) == str:
                c = getattr(self.conn, close_f) # c = def close() ..
                
            c()
            
       
            
            
         
DB_SETTINGS = os.getenv('DB_SETTINGS')
print(DB_SETTINGS)    
db = Database(connection_config=DB_SETTINGS, connector_config={ "connection_method": psycopg2.connect, "connect_method": psycopg2.connect, "close_method": "close" })

db.connection