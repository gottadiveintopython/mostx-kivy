# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
from appglobals import AppGlobals
import scenes.langsettings
from langsettings import LangSettings


def _test():
    appglobals = AppGlobals()
    appglobals.langsettings = LangSettings(
        filepath='./test_langsettings.json'
    )
    root = ScreenManager()
    root.add_widget(
        scenes.langsettings.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)
    # appglobals.langsettings.save()


if __name__ == '__main__':
    _test()
