__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import pkg_gmsh.ext.pygmsh.geometry as pg
import pkg_gmsh.ext.pygmsh.surface_base as surface_base

import yaml
# !/usr/bin/env python3

import caeml.common.tools as tools
import caeml.common.process as process
import logging

import os

from pkg_step.data_model.types import Geometry, SurfaceGroup

class SurfaceGroupsToGeo(tools.PythonTool):
    name = 'asd'
    inputParameters = {'geom_desc': process.Parameter(name='geom_desc', parameterType='pkg_step.data_model.types.Geometry')}
    outputParameters = {'geo_file': process.Parameter(name='geo_file', parameterType='caeml.files.file.File')}

    def launchCmd(self, inputs, tmpStore, stdout_file):
        inputGeometry = inputs['geom_desc']
        assert isinstance(inputGeometry, Geometry)
        geom = pg.Geometry()
        geom.add_merge(inputGeometry.geomFile)
        surfaces = [surface_base.SurfaceBase(item) for item in inputGeometry.surfaces]
        loop = geom.add_surface_loop(surfaces)
        geom.add_volume(loop)

        for group in inputGeometry.surfaceGroups:
            surfaces = []
            for surface in group.surfaceIds:
                surfaces.append(surface_base.SurfaceBase(surface))
            geom.add_physical_surface(surfaces, label=group.name)

        out = geom.get_code()
        with open(tmpStore + '/test.geo', 'w') as f:
            f.write(out)
        logging.getLogger('process_data').debug('Writing: {}'.format(tmpStore + '/test.geo'))
        return {'geo_file': os.path.join(tmpStore + '/test.geo')}