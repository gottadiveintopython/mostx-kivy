# -*- coding: utf-8 -*-
'''
アプリケーション全体を通して共有される、データや関数の入れ物
'''

from attrdict import attrdict

__all__ = ('AppGlobals', )


def _create_dummy_method(name):
    def method(*args, **kwargs):
        print('----------------------', name, args, kwargs, sep='\n')
    return method


def AppGlobals():
    return attrdict(
        records=None,
        langssettings=None,
        quizsettings=None,
        data=attrdict(
            devmode=None,        # type: bool
            mode=None,           # 'timeattack' or 'endless'
            result=None          # result of the quiz
        ),
        funcs=attrdict(**{
            name: _create_dummy_method(name)
            for name in 'play_sound switch_scene'.split()
        })
    )
