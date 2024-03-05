from pymongo import MongoClient

connection_uri = 'mongodb+srv://blavoine:test@cluster0.54fdrky.mongodb.net/'

client = MongoClient(connection_uri)

db = client['Full-stack-back-end']

def get_database():
    return db

def get_users_collection():
    return db['users']

def get_activities_collection():
    return db['activities']

def get_companies_collection():
    return db['companies']

def get_planings_collection():
    return db['planings']


# document = {'key': 'value'}
# collection.insert_one(document)
# client.close()

# Le bloc suivant sera exécuté uniquement si ce fichier est exécuté en tant que script principal
if __name__ == "__main__":
    # Exemple d'utilisation du fichier en tant que script principal
    print("Connecting to the database...")
    database = get_database()
    print("Connected to the database:", database)
    # Vous pouvez ajouter d'autres tests ici si nécessaire