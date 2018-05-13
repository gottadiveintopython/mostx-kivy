# -*- coding: utf-8 -*-

import random
import datetime

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import applicationglobals
import scenes.scene_records
from applicationsettings import Records


def _test():
    appglobals = applicationglobals.create_default()
    appglobals.data.records = records = Records(
        filepath='./test_records.json'
    )
    today = datetime.date.today().isoformat()
    for i in range(3):
        num_cleared = random.randrange(1, 10)
        records.add(
            mode='endless',
            result={
                'date': today,
                'num_cleared': num_cleared,
                'num_answered': 10,
                'languages': 'japanese chinese'.split(),
            }
        )
    for i in range(3):
        time = random.randrange(1, 40)
        records.add(
            mode='timeattack',
            result={
                'date': today,
                'points': round(time * 20 / 25, 2),
                'num_cleared': 20,
                'num_answered': 25,
                'time': time,
                'languages': 'japanese korean'.split(),
            }
        )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_records.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)
    appglobals.data.records.save()


if __name__ == '__main__':
    _test()
