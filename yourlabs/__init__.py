import os

__all__=('VERSION', 'YOURLABS_TEMPLATE')

VERSION='0.0.0'

YOURLABS_TEMPLATE=os.path.realpath(os.path.join(
    os.path.dirname(__file__), 'project_template'))
