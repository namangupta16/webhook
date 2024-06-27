from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['github_events']

def insert_event(event):
    collection = db['events']
    collection.insert_one(event)

def get_latest_events():
    collection = db['events']
    return collection.find().sort('_id', -1).limit(10)
