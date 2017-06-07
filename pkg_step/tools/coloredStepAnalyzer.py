__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import pkg_gmsh.ext.pygmsh.geometry as pg
import pkg_gmsh.ext.pygmsh.surface_base as surface_base

import yaml
# !/usr/bin/env python3

import caeml.common.tools as tools
import caeml.common.process as process
import caeml.common.helper as helper
import logging
from pkg_step.data_model.types import StepGeometry, SurfaceGroup
import os

import pkg_step.data_model.types as types

class StepAnalyzer(tools.PythonTool):
    name = 'asd'
    inputParameters = {'input_step': process.Parameter(name='input_step', parameterType='caeml.files.file.File')}
    outputParameters = {'step': process.Parameter(name='step', parameterType='pkg_step.data_model.types.StepGeometry')}

    def launchCmd(self, inputs, tmpStore, stdout_file):
        helper.runContainer('renumics/python-occ', mounts=[helper.dockerMountDict(tmpStore, '/data')],
                            args=("python3 /scripts/surfaceGroupsFromColoredStep.py /data/input/"
                                 +os.path.basename(inputs['input_step'].path)).split(' '))

        yamlFile = open(os.path.join(tmpStore, 'stepMeta.yml'), 'r')
        yml = yaml.load(yamlFile)
        yamlFile.close()
        groups = {v['name']: v['surfaces'] for v in yml['surfaceGroups']}

        #get flat list of all surfaces stored in groups
        # surfaces = [surface for surfaceList in [k for v, k in groups.items()] for surface in surfaceList]
        surfaces = yml['surfaces']

        step = StepGeometry(geomFile=yml['filename'], surfaces=surfaces, surfaceGroups=groups)
        return {'step': step}