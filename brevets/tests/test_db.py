"""
Nose tests for the new database functionalities of flask_brevets.py

Write your tests HERE AND ONLY HERE.
"""


import nose
import logging
from pymongo import MongoClient

# Works when the Mongo image specified in docker-compose.yml is running
client = MongoClient('mongodb://mongo', 27017)

db = client.mydb

def test_insert():

    # Insert an item into a collection that's new... as far as this program knows...

    db.test_collection.insert_one({
        "foo": "bar",
        "bar": "foo"
    })
    assert(db.test_collection.count_documents({}) == 1)

def test_find():
    item = dict(list(db.test_collection.find())[0])

    # If this statement below is true, then the data placed in the database in the previous test
    # has been properly stored.

    # item['foo'] = 'bar'
    # item['bar'] = 'foo'

    assert(item[item['foo']] == 'foo')

def test_drop():

    # Drop the collection. TESTS MAY FAIL ON RE-RUN IF THIS DOESN'T EXECUTE

    db.drop_collection("test_collection")
    assert(not db.test_collection.count_documents({}))