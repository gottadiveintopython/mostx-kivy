import os.path
import sys

import kivy.resources

sys.path.insert(
    0,
    os.path.join(os.path.pardir, 'mostx')
)
kivy.resources.resource_add_path(
    os.path.join(os.path.pardir, 'mostx', 'data', 'image')
)
kivy.resources.resource_add_path(
    os.path.join(os.path.pardir, 'mostx', 'data', 'text')
)
