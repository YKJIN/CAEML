__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import sys

from jinja2 import Template

if __name__ == '__main__':
    aFolder = sys.argv[1]
    os.makedirs(aFolder)

    env_settings_py_tremplate = Template(
        """
import os
import caeml.management.conf.base

ENVIRONMENT_VARIABLE =  caeml.management.conf.base.ENVIRONMENT_VARIABLE

os.environ[ENVIRONMENT_VARIABLE] =  'settings'
""")

    manage_py_template = Template("""
#!/usr/bin/env python
import sys
import caeml
import settings
caeml.init(settings)

if __name__ == "__main__":
    from caeml.management import execute_from_command_line
    execute_from_command_line(sys.argv)

""")

    settings_py_template = Template("""
import caeml.management.conf  # NOQA

TEST='this is from local test file'
""")

    # file = aFolder + '/' + 'env_settings.py'
    # content = env_settings_py_tremplate.render()
    # with open(file, 'w') as f:
    #     f.write(content)

    file = aFolder + '/' + 'manage.py'
    content = manage_py_template.render()
    with open(file, 'w') as f:
        f.write(content)

    file = aFolder + '/' + 'settings.py'
    content = settings_py_template.render()
    with open(file, 'w') as f:
        f.write(content)

    file = aFolder + '/' + '__init__.py'
    content = settings_py_template.render()
    with open(file, 'w') as f:
        f.write('\n')

    os.makedirs(aFolder + '/caeml_api')
    file = aFolder + '/caeml_api/' + '__init__.py'
    with open(file, 'w') as f:
        f.write('\n')
