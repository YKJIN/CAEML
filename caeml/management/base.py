__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import pkgutil
import sys
from importlib import import_module
from typing import List, Dict


class CommandError(Exception):
    pass


class BaseCommand(object):
    def execute(self, argv):
        raise NotImplementedError('')


def find_commands(management_dir: str) -> List['str']:
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def get_commands() -> Dict['str', 'str']:
    path = os.path.dirname(__file__)
    commands = {name: 'caeml' for name in find_commands(path)}
    return commands


class ManagementUtilityCall(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.commands = get_commands()

    def execute(self):
        subcommand = self.argv[1]
        command_class = self.load_command_class(subcommand)
        command_class.execute(self.argv)

    def load_command_class(self, command_name: str) -> BaseCommand:
        module = import_module('caeml.management.commands.{}'.format(command_name))
        return module.Command()
