import sys
from pathlib import PurePath
ROOT_DIRECTORY = PurePath(__file__).parents[1]
sys.path.insert(1, str(ROOT_DIRECTORY / 'app'))
sys.path.append(str(ROOT_DIRECTORY / 'lib'))


from kivy.resources import resource_add_path
resource_add_path(str(ROOT_DIRECTORY / 'app' / 'data'))
