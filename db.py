import pymongo

mongoURL = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURL)

db = client["MYAPI"]
collection = db["info"]

def create(data):
    data = dict(data)
    response = collection.insert_one(data)
    return str(response.inserted_id)

def all():
    response = collection.find()
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

def get_one(condition):
    response = collection.find_one({"name":condition})
    response["_id"] = str(response["_id"])
    return response