# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import applicationglobals
import scenes.scene_language_settings
from applicationsettings import LanguageSettings


def _test():
    appglobals = applicationglobals.create_default()
    appglobals.data.lang_settings = LanguageSettings(
        filepath='./test_language_settings.json'
    )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_language_settings.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)
    appglobals.data.lang_settings.save()


if __name__ == '__main__':
    _test()
