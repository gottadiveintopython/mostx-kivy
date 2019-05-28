import sys
from pathlib import PurePath

APP_DIR = PurePath(__file__).parents[1] / 'app'
sys.path.append(str(APP_DIR / 'libs'))
sys.path.append(str(APP_DIR))

from kivy.resources import resource_add_path
resource_add_path(str(APP_DIR / 'data'))
