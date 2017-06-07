__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

from bson.dbref import DBRef
from pymongo import MongoClient, database, results, collection

from caeml.management.conf import settings

CONNECTION_NAME = 'db_connection'
_connections = {}
_dbs = {}


def get_connection(con_name: str = CONNECTION_NAME) -> MongoClient:
    if con_name not in _connections:
        _connections[con_name] = MongoClient(
            settings.DATABASE['host'], settings.DATABASE['port'])
    return _connections[con_name]


def get_db(con_name: str = CONNECTION_NAME) -> database.Database:
    if con_name not in _dbs:
        connection = get_connection(con_name)
        _dbs[con_name] = connection[settings.DATABASE['name']]
    return _dbs[con_name]


def create_collection(collection_name: str) -> None:
    collection_names = get_db().collection_names()
    if not collection_name in collection_names:
        collection.Collection(get_db(), collection_name, create=True)


def get_dictById(_id: str, collection_name: str = None) -> dict:
    query = {'_id': _id}
    return get_dictByQuery(query, collection_name)


def get_dictByQuery(query: dict, collection_name: str = None) -> dict:
    collection_names = get_db().collection_names()
    result = None
    if not collection_name is None:
        if not collection_exists(collection_name):
            return None
        result = get_db()[collection_name].find_one(query)
    else:
        for collection_name in collection_names:
            result = get_db()[collection_name].find_one(query)
            if not result is None:
                break

    return result


def add_oneDictIntoCollection(aDict: dict, collection_name: str) -> results.InsertOneResult:
    if not collection_exists(collection_name):
        create_collection(collection_name)
    return get_db()[collection_name].insert_one(aDict)


def replace_oneDictInCollection(aDict: dict, collection_name: str) -> results.UpdateResult:
    if not collection_exists(collection_name):
        raise NameError('Error! the collection "{}" does not exist in the database!'.format(collection_name))
    return get_db()[collection_name].replace_one({'_id': aDict['_id']}, aDict)


def dereference(dbRef: DBRef) -> dict:
    return get_db().dereference(dbRef)


def collection_exists(collection_name: str) -> bool:
    collection_names = get_db().collection_names()
    return collection_name in collection_names
