# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import applicationglobals
import scenes.scene_quiz_endless
from applicationsettings import LanguageSettings, QuizSettings


def _test():
    appglobals = applicationglobals.create_default()
    appglobals.data.update(
        lang_settings=LanguageSettings(
            filepath='./test_language_settings.json'
        ),
        quiz_settings=QuizSettings(
            filepath='./test_quiz_settings.json'
        ),
        devmode=False,
        mode='endless'
    )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_quiz_endless.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)


if __name__ == '__main__':
    _test()
