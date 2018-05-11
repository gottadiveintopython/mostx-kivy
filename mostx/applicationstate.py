# -*- coding: utf-8 -*-
'''
アプリケーション全体を通して共有される、データ及び関数の入れ物
'''

from attrdict import attrdict

__all__ = ('create_default',)


def _create_dummy_method(name):
    def method(*args, **kwargs):
        print('----------------------', name, args, kwargs, sep='\n')
    return method


METHODNAMES = 'play_sound switch_screen'.split()
METHODS = {name: _create_dummy_method(name) for name in METHODNAMES}


def create_default():
    return attrdict(
        data=attrdict(
            records=None,        # type: records.Records
            lang_settings=None,  # type: language_settings.LanguageSettings
            quiz_settings=None,  # type: quiz_settings.QuizSettings
            devmode=None,        # type: bool
            mode=None,           # 'timeattack' or 'endless'
            result=None          # result of the quiz
        ),
        funcs=attrdict(**METHODS)
    )


def _test():
    obj = create_default()
    print(obj.data)
    funcs = obj.funcs
    print(funcs)
    funcs.play_sound('arg', key='value')
    funcs.switch_screen('arg', key='value')


if __name__ == '__main__':
    _test()
