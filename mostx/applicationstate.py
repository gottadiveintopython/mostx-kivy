# -*- coding: utf-8 -*-
r'''
アプリケーション全体を通して共有される、データ及び関数の入れ物
'''

from smartobject import SmartObject

__all__ = (r'create_default',)


def _create_dummy_method(name):
    def method(*args, **kwargs):
        print(r'----------------------', name, args, kwargs, sep='\n')
    return method


METHODNAMES = r'play_sound switch_screen'.split()
METHODS = {name: _create_dummy_method(name) for name in METHODNAMES}


def create_default():
    return SmartObject(
        data=SmartObject(
            so_name=r'applicationstate.data',
            records=None,        # type: records.Records
            lang_settings=None,  # type: language_settings.LanguageSettings
            quiz_settings=None,  # type: quiz_settings.QuizSettings
            devmode=None,        # type: bool
            mode=None,           # 'timeattack' or 'endless'
            result=None          # result of the quiz
        ),
        funcs=SmartObject(so_name=r'applicationstate.functions', **METHODS)
    )


def _test():
    obj = create_default()
    print(obj.data)
    funcs = obj.funcs
    print(funcs)
    funcs.play_sound(r'arg', key=r'value')
    funcs.switch_screen(r'arg', key=r'value')


if __name__ == r'__main__':
    _test()
