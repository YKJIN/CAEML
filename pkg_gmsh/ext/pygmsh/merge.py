# -*- coding: utf-8 -*-
#


class Merge():
    def __init__(self, filepath):
        super(Merge, self).__init__()
        self.filepath = filepath

        self.code = '\n'.join([
            'Merge "{:s}";'.format(filepath)
            ])
        return
