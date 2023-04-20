import requests
from pymongo import MongoClient

# connect to MongoDB database
client = MongoClient("mongodb+srv://sahilpatel:world@cluster.rvmuxrr.mongodb.net/?retryWrites=true&w=majority")
db = client["Countries"]
collection = db["countries"]

# clear existing data from collection
collection.delete_many({})

# fetch data from REST Countries API
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
data = response.json()

# insert data into MongoDB collection
for entry in data:
    collection.insert_one(entry)
