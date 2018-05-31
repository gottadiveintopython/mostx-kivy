# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import scenes.result
from attrdict import attrdict
from appglobals import AppGlobals
from records import Records


def _test():
    appglobals = AppGlobals()
    appglobals.update(
        records=Records(filepath='./test_records.json'),
    )
    appglobals.data.update(
        devmode=False,
        mode='timeattack',
        result=attrdict(
            points=12.34,
            n_cleared=20,
            n_answered=37,
            time=123,
            langs=['python'],
        ),
    )
    root = ScreenManager()
    root.add_widget(
        scenes.result.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)


if __name__ == '__main__':
    _test()
