
# import os
# import sys 
# import json
# from dotenv import load_dotenv
# from pymongo.mongo_client import MongoClient

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# from network_security.logging import logging
# from network_security.exception import NetworkSecurityException
# import certifi


# load_dotenv()




# MONGO_DB_URI=os.getenv("MongoDB_url")
# username=os.getenv("username")
# password=os.getenv("password")


import certifi
import pandas as pd
import numpy as np
import pymongo

# class NetworkDataExtract():
#     def __init__(self):
#         try:
#             pass
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def cv_to_json_converter(self,file_path):
        
#         try:
#             data=pd.read_csv(file_path)
#             data.reset_index(drop=True,inplace=True)
#             records=list(json.loads(data.T.to_json()).values())
#             return records
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def insert_data_MongoDB(self,records,collection,database):
#         try:
#             self.records=records
#             self.database=database
#             self.collection=collection
            
            
#             self.mongo_client =  MongoClient(f"mongodb+srv://{username}:{password}@cluster.7tj79jr.mongodb.net/dbname?retryWrites=true&w=majority",ssl=True,
#                         tlsAllowInvalidCertificates=True )
#             self.database= self.mongo_client[self.database]
            
#             self.collection=self.database[self.collection]
#             self.collection.insert_many(self.records)
            
#             return (len(self.records))
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
        
# if __name__=="__main__":
#     FILE_PATH='Network_data\phisingData.csv'
#     Collection='NetworkData'
#     Database='hardikkhobragade78'
#     network_obj=NetworkDataExtract()
#     records=network_obj.cv_to_json_converter(FILE_PATH)
#     print(records)
#     no_of_records=network_obj.insert_data_MongoDB(records=records,collection=Collection,database=Database)
#     print(no_of_records)


import os
import sys 
import json
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi  # For proper SSL certificate validation

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from network_security.logging import logging
from network_security.exception import NetworkSecurityException

load_dotenv()

MONGO_DB_URI = os.getenv("MongoDB_url")
username = os.getenv("username")
password = os.getenv("password")

uri = f"mongodb+srv://{username}:{password}@cluster0.7tj79jr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class NetworkDataExtract():
    def __init__(self):
        try:
           
            self.mongo_client =MongoClient(uri, server_api=ServerApi('1'))
            self.mongo_client.admin.command('ping')
            logging.info("Successfully connected to MongoDB!")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def cv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_MongoDB(self, records, collection, database):
        try:
            db = self.mongo_client[database]
            col = db[collection]
            result = col.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
if __name__ == "__main__":
    FILE_PATH = 'Network_data/phisingData.csv'  
    Collection = 'NetworkData'
    Database = 'hardikkhobragade78'
    
    try:
        network_obj = NetworkDataExtract()
        records = network_obj.cv_to_json_converter(FILE_PATH)
        print(f"Converted {len(records)} records")
        no_of_records = network_obj.insert_data_MongoDB(
            records=records,
            collection=Collection,
            database=Database
        )
        print(f"Successfully inserted {no_of_records} records")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        
