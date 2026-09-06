import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient
load_dotenv()

client = AsyncMongoClient(os.environ["MONGODB_URL"])
db = client.abrikoz
