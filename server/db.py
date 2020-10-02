from flask import Flask
import os
from flask_pymongo import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://"+ os.environ['abc'] +":" + os.environ['PASSWORD'] +"@intellimind.yxcn8.mongodb.net/intellimind?retryWrites=true&w=majority"
print("@@@@@@@@@@@@@@@@@@@2",CONNECTION_STRING)
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('test')
store = pymongo.collection.Collection(db, 'intelli')
# print(os.environ['AWS_ACCESS_KEY_ID'])