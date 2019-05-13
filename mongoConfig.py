import pymongo
from pymongo import MongoClient

host = 'localhost'
port = 27017

def connectMongo():
    client = MongoClient('localhost', 27017)
    db = client['stackoverflow']
    return db

def getCollection(collection, db):
    collection = db[collection]
    return collection