from pymongo import MongoClient

connection_uri = 'mongodb+srv://blavoine:test@cluster0.54fdrky.mongodb.net/'

client = MongoClient(connection_uri)

db = client['Full-stack-back-end']

collection = db['your_collection_name']


document = {'key': 'value'}
collection.insert_one(document)

# client.close()