from pymongo import MongoClient
import re

# Requires the PyMongo package.
# https://api.mongodb.com/python/current
client = MongoClient('mongodb://localhost:27017/')

db = client['todolist_db']  # Sélection de la base de données
tasks_collection = db['tasks']  # Sélection de la collection

filter={}

tasks = tasks_collection.find(
  filter=filter,
  sort=['nom']
)