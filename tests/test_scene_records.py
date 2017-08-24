# -*- coding: utf-8 -*-

import random
import datetime

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import applicationstate
import scenes.scene_records
from applicationsettings import Records


def _test():
    appstate = applicationstate.create_default()
    appstate.data.records = records = Records(
        filepath=r'./test_records.json'
    )
    today = datetime.date.today().isoformat()
    for i in range(3):
        num_cleared = random.randrange(1, 10)
        records.add(
            mode=r'endless',
            result={
                r'so_name': r'record',
                r'date': today,
                r'num_cleared': num_cleared,
                r'num_answered': 10,
                r'languages': r'japanese chinese'.split(),
            }
        )
    for i in range(3):
        time = random.randrange(1, 40)
        records.add(
            mode=r'timeattack',
            result={
                r'so_name': r'record',
                r'date': today,
                r'points': round(time * 20 / 25, 2),
                r'num_cleared': 20,
                r'num_answered': 25,
                r'time': time,
                r'languages': r'japanese korean'.split(),
            }
        )
    root = ScreenManager()
    root.add_widget(
        scenes.scene_records.instantiate(appstate=appstate)
    )
    runTouchApp(root)
    appstate.data.records.save()


if __name__ == r'__main__':
    _test()
