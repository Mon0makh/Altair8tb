from pymongo import MongoClient

from config import MONGODB_LINK
from config import MONGO_DB

import certifi

import logging

ca = certifi.where()
mondb = MongoClient(MONGODB_LINK, tlsCAFile=ca)[MONGO_DB]

users = mondb.users.find()

for user in users:
    mondb.users.update_one(
        {'_id': user['_id']},
        {'$set':
             {'user_hubs': 1111110}})

print("done")