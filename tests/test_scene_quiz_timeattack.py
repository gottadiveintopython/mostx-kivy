# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import applicationstate
import scenes.scene_quiz_timeattack
from applicationsettings import LanguageSettings, QuizSettings


def _test():
    appstate = applicationstate.create_default()
    appstate.data.so_overwrite(
        lang_settings=LanguageSettings(
            filepath=r'./test_language_settings.json'
        ),
        quiz_settings=QuizSettings(
            filepath=r'./test_quiz_settings.json'
        ),
        devmode=False,
        mode=r'timeattack'
    )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_quiz_timeattack.instantiate(appstate=appstate)
    )
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
