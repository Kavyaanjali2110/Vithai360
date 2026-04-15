from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["vithai360"]

users = db["users"]
predictions = db["predictions"]