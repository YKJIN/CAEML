__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import pkg_gmsh.ext.pygmsh.geometry as pg
import pkg_gmsh.ext.pygmsh.surface_base as surface_base

import yaml
# !/usr/bin/env python3

import caeml.common.tools as tools
import caeml.common.process as process
import caeml.common.helper as helper
from caeml.files.file import File

import os
import re

class MeshGeoGmsh(tools.PythonTool):
    name = 'asd'
    inputParameters = {'geo': process.Parameter(name='geo', parameterType='caeml.files.file.File'),
                       'mergedFile': process.Parameter(name='mergedFile', parameterType='caeml.files.file.File'),
                       'clscale': process.Parameter(name='clscale', parameterType='float')}
    outputParameters = {'med': process.Parameter(name='med', parameterType='caeml.files.file.File'),
                        'mesh': process.Parameter(name='mesh', parameterType='caeml.files.file.File'),
                        'msh': process.Parameter(name='msh', parameterType='caeml.files.file.File'),
                        'ply2': process.Parameter(name='ply2', parameterType='caeml.files.file.File'),
                        'stl': process.Parameter(name='stl', parameterType='caeml.files.file.File'),
                        'unv': process.Parameter(name='unv', parameterType='caeml.files.file.File'),
                        'vrml': process.Parameter(name='vrml', parameterType='caeml.files.file.File'),
                        'elemCount': process.Parameter(name='elem_count', parameterType='int'),
                        'vertCount': process.Parameter(name='vert_count', parameterType='int')}

    def launchCmd(self, inputs, tmpStore, stdout_file):

        gmshCommand = "gmsh -3 {} -v 10 -clscale {:f} -o /data/mesh.msh".format('/data/input/' + os.path.basename(inputs['geo'].path),
                                                                               inputs['clscale'])

        helper.runContainer('renumics/gmsh', mounts=[helper.dockerMountDict(tmpStore, '/data')],
                            args=gmshCommand.split(' '), stdout_file=stdout_file)

        with open(stdout_file, 'r') as stdoutF:
            res = stdoutF.read()

        regexp = re.compile('(\d+) vertices (\d+) elements')
        m = re.findall(regexp, res)
        vertsCount = m[-1][0]
        elemCount = m[-1][1]

        # convert to other output files
        gmshCommand = "gmsh /data/mesh.msh /scripts/convert -"

        helper.runContainer('renumics/gmsh', mounts=[helper.dockerMountDict(tmpStore, '/data')],
                            args=gmshCommand.split(' '), stdout_file=stdout_file)

        return {'med': os.path.join(tmpStore, 'mesh.med'),
                'mesh': os.path.join(tmpStore, 'mesh.mesh'),
                'msh': os.path.join(tmpStore, 'mesh.msh'),
                'ply2': os.path.join(tmpStore, 'mesh.ply2'),
                'stl': os.path.join(tmpStore, 'mesh.stl'),
                'unv': os.path.join(tmpStore, 'mesh.unv'),
                'vrml': os.path.join(tmpStore, 'mesh.vrml'),
                'elemCount': elemCount, 'vertCount': vertsCount}
