# db.py
from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://martinjauma:Piston@clustergd.qny9kpp.mongodb.net/")
    db = client["gestDep_db_json"]
    return db


