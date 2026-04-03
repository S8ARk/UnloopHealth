import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self, uri=None):
        self.uri = uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017/nutricore')
        self.client = None
        self.db = None

    def connect(self):
        try:
            # Use certifi for SSL/TLS verification
            ca = certifi.where()
            self.client = MongoClient(self.uri, tlsCAFile=ca)
            
            # Explicitly check for the default database if specified in the URI
            default_db = self.client.get_default_database()
            if default_db is not None:
                self.db = default_db
            else:
                self.db = self.client['nutricore']
                
            # Ping the database to check connectivity
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return False

    def get_collection(self, collection_name):
        if self.db is None:
            self.connect()
        return self.db[collection_name]

    def get_user_profile(self, user_id):
        return self.get_collection('users').find_one({"_id": user_id})

    def update_user_profile(self, user_id, profile_data):
        return self.get_collection('users').update_one(
            {"_id": user_id},
            {"$set": {"profile": profile_data}}
        )

    def log_activity(self, user_id, activity_data):
        """ Log daily activity: water, sleep, screen time, etc. """
        return self.get_collection('activity_logs').update_one(
            {"user_id": user_id, "date": activity_data['date']},
            {"$set": activity_data},
            upsert=True
        )

# Global instance
db_instance = Database()

def get_db():
    if db_instance.db is None:
        db_instance.connect()
    return db_instance.db
