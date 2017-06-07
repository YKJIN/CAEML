__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"

from importlib import import_module

import caeml.common.db
import caeml.common.process
import caeml.common.tools


def getCmdTool(tool_name: str) -> caeml.common.process.Process:
    """create tool instance from a _____ test file"""

    data = caeml.common.db.get_dictByQuery({"name": tool_name}, 'caeml.common.tools')
    if data is None:
        # TODO make thos block work for all tools
        if (tool_name == 'add'):
            tool_name = 'caeml.tools.add.add'
        p, m = tool_name.rsplit('.', 1)
        mod = import_module(p)
        met = getattr(mod, m)
        return met()
    else:
        tool = caeml.common.base.constructCaemlObj_fromCaemlDict(data)
    return tool

    # TODO: generalize
