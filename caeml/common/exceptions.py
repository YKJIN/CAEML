__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"


class ImproperlyConfigured(Exception):
    """CAEML is somehow improperly configured"""
    pass


class DBJSONException(Exception):
    """Cannot serialize to JSON, base classes must implement the default method"""
    pass


class NotRegistered(Exception):
    """Class not registered in DB"""
    pass


class InitDBException(Exception):
    """A problem has occured during db initialization"""
    pass
