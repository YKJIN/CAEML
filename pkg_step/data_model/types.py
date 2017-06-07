__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
from typing import Dict, List

from caeml.files.file import File


class SurfaceGroup():

    def __init__(self, groupName, surfaceIds: List[int]):
        self.name = groupName
        self.surfaceIds = surfaceIds


class Geometry():

    def __init__(self, geomFile: File, surfaces: list = None, surfaceGroups: Dict['str', 'list']=None):
        self.geomFile = geomFile
        self.surfaceGroups = [SurfaceGroup(k, v) for k, v in surfaceGroups.items()]
        self.surfaces = surfaces


class StepGeometry(Geometry):

    def __init__(self, geomFile: File, surfaces: list = None, surfaceGroups: Dict['str', 'list'] = None):
        super(StepGeometry, self).__init__(geomFile=geomFile, surfaces=surfaces, surfaceGroups=surfaceGroups)
