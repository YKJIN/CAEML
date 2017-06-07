__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
"""
Inspired from django.core.files.base.File and django.core.files.base.ContentFile
https://github.com/django/django/blob/master/django/core/files/base.py
"""
import os


class File(object):
    def __init__(self, path: str):
        self.path = path

    def open(self, mode=None):
        if not self.closed:
            self.seek(0)
        elif self.path and os.path.exists(self.path):
            self.file = open(self.path, mode)
        else:
            raise ValueError("The file cannot be reopened.")

    def close(self):
        self.file.close()

    def getFileBaseName(self) -> str:
        return os.path.basename(self.path)
