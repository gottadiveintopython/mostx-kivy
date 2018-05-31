# -*- coding: utf-8 -*-

import beforetest
from appglobals import AppGlobals


def _test():
    obj = AppGlobals()
    print(obj.data)
    funcs = obj.funcs
    print(funcs)
    funcs.play_sound('arg', key='value')
    funcs.switch_scene('arg', key='value')


if __name__ == '__main__':
    _test()
