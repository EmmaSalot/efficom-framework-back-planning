"""Module defining database connection and initialization"""

# Libs imports
from pymongo import MongoClient

# Connection URI for MongoDB
connection_uri = 'mongodb+srv://blavoine:test@cluster0.54fdrky.mongodb.net/'

# Initialize MongoClient
client = MongoClient(connection_uri)

# Access the database
db = client['Full-stack-back-end']

def initialize_database():
    """
    Initialize database connection
    """
    print("Connecting to the database...")
    database = get_database()
    print("Connected to the database:", database)

def get_database():
    """Get the current database"""
    return db

def get_users_collection():
    """Get the users collection from the database"""
    return db['users']

def get_activities_collection():
    """Get the activities collection from the database"""
    return db['activities']

def get_companies_collection():
    """Get the companies collection from the database"""
    return db['companies']

def get_planings_collection():
    """Get the plannings collection from the database"""
    return db['plannings']


# The following block will be executed only if this file is executed as the main script
if __name__ == "__main__":
    # Example of using the file as the main script
    print("Connecting to the database...")
    database = get_database()
    print("Connected to the database:", database)
    # You can add more tests here if needed
