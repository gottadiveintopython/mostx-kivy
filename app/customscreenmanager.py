# -*- coding: utf-8 -*-

__all__ = ('MostxScreenManager', )
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition


class MostxScreenManager(ScreenManager):
    '''
    Screenの切り替えを代入文(current属性への代入)で行うのに違和感があるので、Method
    呼び出しにて行うようにした。
    '''

    def switch_screen(self, name, transition=NoTransition()):
        self.transition = transition
        self.current = name


# class MostxScreenForNesting(Screen):
#     '''ScreenManagerを入れ子にする際に間に挟むScreen

#     on_pre_enter(), on_enter(), on_pre_leave(), on_leave()の四つのMethodの呼び出
#     しの伝搬を行う'''
#     pass


# for name in 'on_pre_enter on_enter on_pre_leave on_leave'.split():
#     def proxy(self, _name=name, *args, **kwargs):
#         method = getattr(self.children[0], _name, None)
#         if method is not None:
#             return method(*args, **kwargs)
#     setattr(MostxScreenForNesting, name, proxy)
