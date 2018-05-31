# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
from appglobals import AppGlobals
import scenes.credits


def _test():
    root = ScreenManager()
    root.add_widget(
        scenes.credits.instantiate(appglobals=AppGlobals())
    )
    runTouchApp(root)


if __name__ == '__main__':
    _test()
