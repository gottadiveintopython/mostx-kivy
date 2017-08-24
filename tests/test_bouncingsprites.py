# -*- coding: utf-8 -*-

import kivy.resources
from kivy.base import runTouchApp

import beforetest
from scenes.bouncingsprites import BouncingSprites


def _test():
    root = BouncingSprites(
        atlasfilepath=kivy.resources.resource_find(r'characters.atlas'),
        size=(800, 600,)
    )
    root.start_animation()

    runTouchApp(root)


if __name__ == r'__main__':
    _test()
