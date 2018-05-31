# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
from appglobals import AppGlobals
import scenes.quiz_timeattack
from langsettings import LangSettings
from quizsettings import QuizSettings


def _test():
    appglobals = AppGlobals()
    appglobals.update(
        langsettings=LangSettings('./test_langsettings.json'),
        quizsettings=QuizSettings('./test_quizsettings.json'),
    )
    appglobals.data.update(
        devmode=True,
        mode='timeattack',
    )
    root = ScreenManager()
    root.add_widget(
        scenes.quiz_timeattack.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)


if __name__ == '__main__':
    _test()
