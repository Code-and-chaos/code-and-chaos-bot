import pymongo
import json

# Load MongoDB configuration from config.json
with open('config.json') as f:
    config_data = json.load(f)
    mongo_config = config_data.get('mongoDB', {})
    mongo_host = mongo_config.get('host')
    mongo_database = mongo_config.get('database')
    mongo_user = mongo_config.get('user')
    mongo_password = mongo_config.get('password')

class MongoAPI:
    def __init__(self, db_name):
        if mongo_user and mongo_password:
            self.client = pymongo.MongoClient(mongo_host, username=mongo_user, password=mongo_password)
        else:
            self.client = pymongo.MongoClient(mongo_host)
        self.db = self.client[db_name]
        self.db.settings
        self.db.users


    def get_setting(self, setting_name):
        settings_collection = self.db.settings
        result = settings_collection.find_one({'name': setting_name})
        if result:
            return result.get('value')
        else:
            return None

    def set_setting(self, setting_name, value):
        settings_collection = self.db.settings
        settings_collection.update_one({'name': setting_name}, {'$set': {'value': value}}, upsert=True)

    def get_user(self, user_id):
        users_collection = self.db.users
        result = users_collection.find_one({'user_id': user_id})
        if result:
            return result
        else:
            return None

    def set_user(self, user_id, data):
        users_collection = self.db.users
        users_collection.update_one({'user_id': user_id}, {'$set': data}, upsert=True)

    def delete_user(self, user_id):
        users_collection = self.db.users
        users_collection.delete_one({'user_id': user_id})

    def level_up(self, user_id):
        users_collection = self.db.users
        users_collection.update_one({'user_id': user_id}, {'$inc': {'level': 1}})
