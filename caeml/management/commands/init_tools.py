__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import importlib
import logging
import os
import uuid

import yaml

from caeml.common.db import get_dictByQuery, add_oneDictIntoCollection, replace_oneDictInCollection, create_collection
from caeml.management.base import BaseCommand
from caeml.management.conf import settings


class Command(BaseCommand):
    help = "Initializes Tools from settings files"

    def execute(self, argv):
        # create logging directories

        self.inserted_names = []

        tools = settings.TOOLS

        for tools_location in tools:
            module_path = os.path.dirname(importlib.import_module(tools_location).__file__)
            for tool_path in os.listdir(module_path):
                if tool_path.endswith('.py'):
                    # python tool
                    pass
                if tool_path.endswith('.yml') or tool_path.endswith('.yaml'):
                    # other tool
                    self.initCmdTool(os.path.join(module_path, tool_path))

    def initCmdTool(self, path: str):
        create_collection('caeml.common.tools')
        try:
            with open(path, 'r') as f:
                data = yaml.load(f)
            if not 'dockerImageId' in data:
                data['baseCommand'] = \
                    os.path.abspath(os.path.join(os.path.dirname(path), data['baseCommand'].format(path)))
            elif 'scriptPath' in data:
                data['scriptPath'] = os.path.abspath(os.path.join(os.path.dirname(path), data['scriptPath']))
            for k, v in data['inputParameters'].items():
                v['caemlType'] = 'caeml.common.process.Parameter'
                if 'inputBinding' in v:
                    v['inputBinding']['caemlType'] = "caeml.common.process.InputBinding"
                if '[]' == v['parameterType'] or isinstance(v['parameterType'],
                                                            list):  # TODO: allow typed list (eg int[])
                    v['parameterType'] = 'list'
                if 'file' == v['parameterType']:
                    v['parameterType'] = 'caeml.files.file.File'
            for k, v in data['outputParameters'].items():
                v['caemlType'] = "caeml.common.process.Parameter"
                if 'outputBinding' in v:
                    v['outputBinding']['caemlType'] = "caeml.common.process.OutputBinding"
                if '[]' == v['parameterType'] or isinstance(v['parameterType'], list):
                    v['parameterType'] = 'list'
                if 'file' == v['parameterType']:
                    v['parameterType'] = 'caeml.files.file.File'

            if not 'name' in data:
                raise LookupError("YAML file needs to specify tool name for tool at path: {}".format(path))
        except Exception as e:
            raise Exception("Error from Tool: {}: {}".format(path, str(e)))

        loaded_data = get_dictByQuery({"name": data['name']}, 'caeml.common.tools')
        if loaded_data is None:
            data['_id'] = str(uuid.uuid4())
            add_oneDictIntoCollection(data, 'caeml.common.tools')
        else:
            data['_id'] = loaded_data['_id']
            replace_oneDictInCollection(data, 'caeml.common.tools')

        if data['name'] in self.inserted_names:
            logging.getLogger('init').warning(
                "Tool with name: {} already exists in database and has been overwritten".format(data['name']))
        self.inserted_names.append(data['name'])
        pass
