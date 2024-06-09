import pymongo

def mongo_db_verbinden():
    # Verbindung zur MongoDB herstellen
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ARo_Datenbank"]
    mycol = mydb["Turnier_Sammlung"]
    
    return mycol
