import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cat_database"]
collection = db["cats"]

def create_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f"Created cat with id: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"An error occurred: {e}")

def read_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Updated age of cat with name: {name}")
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_cat_feature(name, feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print(f"Added feature to cat with name: {name}")
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Deleted cat with name: {name}")
        else:
            print(f"No cat found with name: {name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} cats")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Приклад використання функцій
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_cat_feature("barsik", "любить грати з м'ячиком")
    delete_cat_by_name("barsik")
    delete_all_cats()
