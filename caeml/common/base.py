__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

import copy
import logging
import uuid
from builtins import Exception
from pydoc import locate
from typing import Dict

from bson.dbref import DBRef

from caeml.common.db import add_oneDictIntoCollection, replace_oneDictInCollection, dereference, get_dictById

"""this module provides serialization/deserialization methods for objects in caeml.common"""


class caemlBaseObj(object):
    """this base class for classes in caeml.common provides serialization methods"""

    def getCaemlDict_Recursive(self) -> dict:
        aCaemlDict = dict([(x, copy.deepcopy(y)) for x, y in
                           self.__dict__.items() if (
                               not x.startswith('_') and not x.startswith('parent')) or x.startswith('_id')])
        if 'caemlType' in aCaemlDict:
            raise Exception('caemlType is reserved and cannot be used in a caeml serializable obj')
        else:
            aCaemlDict['caemlType'] = [t.__module__ + '.' + t.__name__ for t in type(self).mro()]

        for k, v in aCaemlDict.items():
            if type(v) in [dict]:
                for k2, v2 in v.items():
                    if isinstance(v2, caemlBaseObj):
                        aCaemlDict[k][k2] = v2.getCaemlDict_Recursive()
            if type(v) in [list]:
                for i, v2 in enumerate(v):
                    if isinstance(v2, caemlBaseObj):
                        aCaemlDict[k][i] = v2.getCaemlDict_Recursive()

            elif isinstance(v, caemlBaseObj):
                aCaemlDict[k] = v.getCaemlDict_Recursive()
            else:
                pass  # keep entry

        return aCaemlDict


class caemlNodeObj(caemlBaseObj):
    def __init__(self, name: str = None, parent: caemlBaseObj = None):
        self.name = name
        self.parent = parent
        super().__init__()


class caemlDBObj(caemlBaseObj):
    def __init__(self, _id: str = None):
        self._id = _id if _id else str(uuid.uuid4())
        super().__init__()

    def save(self) -> str:
        collection = self.__class__.collectionName()

        aDict = self.getCaemlDict_Recursive()
        aDict = self.createObjectReferencesRecursive(aDict)
        return self._id

    """Store a caeml dict to db. Only store a dbref for nested dicts of caemlDBObjs"""

    def createObjectReferencesRecursive(self, data):
        if isinstance(data, dict):
            aDict = data
            new_dict = {}

            if "_id" in data:  # data is a DB Object: Store as data only as DBRef
                # check data for more potential db_refs and remove them before this data dict is stored.
                for k, v in data.items():
                    new_dict[k] = self.createObjectReferencesRecursive(v)
                assert new_dict['_id'] is not None, "if objects _id is set it is not allowed to be None"
                ref = DBRef(str(new_dict['caemlType'][0]), new_dict['_id'])
                res = dereference(ref)  # is referenced object already in the db?
                if res is None:
                    add_oneDictIntoCollection(new_dict, ref.collection)
                else:
                    replace_oneDictInCollection(new_dict, ref.collection)
                return ref

            else:  # check nested dicts items for potentials DBRefs
                for k, v in data.items():
                    new_dict[k] = self.createObjectReferencesRecursive(v)
                return new_dict


        elif isinstance(data, list):  # check nested list items for potentials DBRefs
            new_list = [self.createObjectReferencesRecursive(l) for l in data]
            return new_list

        else:  # data is not a dict
            return data

    @classmethod
    def load(self, pk: str) -> caemlBaseObj:
        dict = get_dictById(pk)
        obj = constructCaemlObj_fromCaemlDict(dict)
        return obj

    @classmethod
    def load_DBRef(self, aDBRef: DBRef) -> 'caemlDBObj':
        if type(aDBRef) is dict:
            raise ValueError('load_DBRef: No valid DBRef object provided')
        aDictRes = dereference(aDBRef)
        assert (aDictRes)
        return constructCaemlObj_fromCaemlDict(aDictRes)

    @classmethod  # used to find a mongo-db collection for a type
    def collectionName(self) -> str:
        return self.mro()[0].__module__ + '.' + self.mro()[0].__name__


def constructCaemlObjs_fromCaemlDicts(aDict: dict, parent: caemlBaseObj) -> Dict[str, caemlBaseObj]:
    """Construct a dict with caeml-objects of given type"""
    if 'caemlType' in aDict:
        aDict.pop('caemlType')
    logging.getLogger('system').debug(aDict)
    for key, value in aDict.items():
        if 'name' in value:
            value.pop('name')
        assert 'parent' not in value
    aDictCreated = {key: constructCaemlObj_fromCaemlDict({'name': key, 'parent': parent, **value})
                    for key, value in aDict.items()}
    return aDictCreated


# TODO manager: move to class method (djangos manager-style)
def constructCaemlObj_fromCaemlDict(aDict: dict) -> caemlBaseObj:
    """Constructs a object of caeml.base from a dict if caeml knows how to contruct, else aDict is returned."""
    if not 'caemlType' in aDict:
        raise ValueError('aDict must include a CAEMl type')
    aClassName = aDict.pop('caemlType')
    if not type(aClassName) is list:
        aClassName = [aClassName]
    logging.getLogger('system').debug('Building object of type' + aClassName[0])
    aClass = locate(aClassName[0])  # TODO manager autocomplete, TODO: manager
    if (not aClass):
        raise Exception('No ctor found for ' + aClassName[0])

    try:
        if 'name' in aDict:
            aObject = aClass(**aDict)  # TODO: maybe validate parent<-> child relationships here:
        else:
            aObject = aClass(**aDict)
        return aObject
    except Exception as e:
        raise Exception('Ctor of {} raised {}'.format(aClassName[0], str(e)))
