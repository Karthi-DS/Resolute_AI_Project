import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("uri")
print(uri)

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.user
collection_name = db["users"]