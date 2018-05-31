# -*- coding: utf-8 -*-

import random
import datetime

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
from appglobals import AppGlobals
from records import Records
import scenes.records


def _test():
    # 無作為にQuizの成績を作る
    random_random = random.random
    random_randrange = random.randrange
    random_sample = random.sample
    LANGS = 'Japanese Chinese Korean English'.split()
    LEN_LANGS_PLUS1 = len(LANGS) + 1
    records = Records(
        filepath='./test_records.json'
    )
    today = datetime.date.today().isoformat()
    for i in range(50):
        n_answered = random_randrange(10, 20)
        records.add(
            mode='endless',
            result={
                'date': today,
                'n_cleared': random_randrange(0, n_answered),
                'n_answered': n_answered,
                'langs': random_sample(LANGS, random_randrange(1, LEN_LANGS_PLUS1)),
            }
        )
    for i in range(50):
        time = random_random() * 300
        n_answered = random_randrange(10, 20)
        n_cleared = random_randrange(0, n_answered)
        records.add(
            mode='timeattack',
            result={
                'date': today,
                'points': round(time * n_cleared / n_answered, 2),
                'n_cleared': n_cleared,
                'n_answered': n_answered,
                'time': time,
                'langs': random_sample(LANGS, random_randrange(1, LEN_LANGS_PLUS1)),
            }
        )
    #
    appglobals = AppGlobals()
    appglobals.records = records
    root = ScreenManager()
    root.add_widget(
        scenes.records.instantiate(appglobals=appglobals)
    )
    runTouchApp(root)
    # appglobals.records.save()


if __name__ == '__main__':
    _test()
