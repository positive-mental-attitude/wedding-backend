#!/usr/bin/env python3
"""
Database initialization script for the Afterparty RSVP application (MongoDB version).
This script checks MongoDB connection and ensures the 'afterparty' collection exists.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://<username>:<password>@<cluster-url>/wedding?retryWrites=true&w=majority')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

def main():
    print("Checking MongoDB connection and 'afterparty' collection...")
    try:
        client.admin.command('ping')
        # Optionally, create a dummy document and delete it to ensure collection exists
        test_doc = {'test': True}
        result = db['afterparty'].insert_one(test_doc)
        db['afterparty'].delete_one({'_id': result.inserted_id})
        print("MongoDB connection successful. 'afterparty' collection is ready.")
        return 0
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return 1

if __name__ == '__main__':
    exit(main()) 