# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import scenes.scene_result
from attrdict import attrdict
import applicationglobals
from applicationsettings import Records


def _test():
    appglobals = applicationglobals.create_default()
    appglobals.data.update(
        records=Records(filepath='./test_records.json'),
        devmode=False,
        mode='timeattack',
        result=attrdict(
            points=12.34,
            num_cleared=20,
            num_answered=37,
            time=123,
            languages=['python'],
        )
    )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_result.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)


if __name__ == '__main__':
    _test()
