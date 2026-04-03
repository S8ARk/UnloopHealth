import os
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
            self.client = MongoClient(self.uri)
            # Access the database specified in the URI or default to 'nutricore'
            self.db = self.client.get_default_database() or self.client['nutricore']
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

# Global instance
db_instance = Database()

def get_db():
    if db_instance.db is None:
        db_instance.connect()
    return db_instance.db
