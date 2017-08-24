# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import scenes.scene_result
from smartobject import SmartObject
import applicationstate
from applicationsettings import Records


def _test():
    appstate = applicationstate.create_default()
    appstate.data.so_overwrite(
        records=Records(filepath=r'./test_records.json'),
        devmode=False,
        mode=r'timeattack',
        result=SmartObject(
            points=12.34,
            num_cleared=20,
            num_answered=37,
            time=123,
            languages=[r'python'],
        )
    )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_result.instantiate(appstate=appstate)
    )
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
