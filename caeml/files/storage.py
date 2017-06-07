__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import glob
import os
from typing import List

from caeml.management.conf import settings


class FileStorage(object):
    """
    A file storage class, providing functionality for storing and loading files to some defined location.
    """

    def __init__(self, baseLocation: str = ""):
        self.setBaseLocation(baseLocation)

    def setBaseLocation(self, baseLocation_in: str):
        data_dir = os.path.join(os.path.expanduser(settings.DATA_DIR), settings.FILES_DIR_SUFFIX)
        self._baseLocation = os.path.join(data_dir, baseLocation_in)
        assert (os.path.isdir(self._baseLocation))

    def resetBaseLocationToNewSub(self, name: str):
        """ Generate a new folder make sure it is unique by adding a number > 0"""
        currentDir = os.path.join(os.path.expanduser(settings.DATA_DIR), settings.FILES_DIR_SUFFIX)
        assert (os.path.isdir(currentDir))
        i = 1
        new_folder = self.path(name)
        while self.exists(new_folder):
            new_folder = self.path(name + '_' + str(i))
            i = i + 1
        os.mkdir(new_folder)
        self._baseLocation = new_folder

    def addSub(self, name: str):
        if '/' in name:
            raise (NotImplementedError())
        os.mkdir(self.path(name))

    @property
    def baseLocation(self) -> str:
        return self._baseLocation

    def path(self, name: str) -> str:
        return os.path.join(self.baseLocation, name)

    def exists(self, name: str) -> bool:
        return os.path.exists(self.path(name))

    def glob(self, pathname: str) -> List['str']:
        return glob.glob(self.path(pathname))

    def ls(self, ls_path="", ext="") -> List['str']:
        return [f for f in os.listdir(self.path(ls_path)) if f.endswith(ext)]

    def delete(self, name):
        os.remove(self.path(name))  # fails if file does not exist
