from flask_pymongo import PyMongo
from pymongo import MongoClient

mongo_client = None

def create_mongo_client():
    global mongo_client
    mongo_client = MongoClient("mongodb://localhost:27017")
    print("Connected to MongoDB")
    return mongo_client["mydatabase"]

def get_db():
    return mongo_client["mydatabase"] if mongo_client else None