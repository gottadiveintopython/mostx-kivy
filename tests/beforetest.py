import sys
import os
from os.path import (
    abspath as ospath_abspath,
    dirname as ospath_dirname,
    pardir as ospath_pardir,
    join as ospath_join,
)

from kivy.resources import resource_add_path


ROOT_DIRECTORY = ospath_abspath(ospath_join(
    ospath_dirname(sys.modules[__name__].__file__),
    ospath_pardir,
    'mostx',
))
sys.path.append(ROOT_DIRECTORY)


for parent, __1, __2 in os.walk(ospath_join(ROOT_DIRECTORY, 'data')):
    resource_add_path(parent)
