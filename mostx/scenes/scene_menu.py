# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, FadeTransition

import customwidgets

__all__ = ('instantiate',)
KV_CODE = r"""
<MenuItem@BorderedButton>:

<MenuScreen>:
    name: 'menu'
    ScrollView:
        GridLayout:
            size_hint: 1, None
            height: self.minimum_height
            cols: 1
            row_default_height: 50
            row_force_default: True
            padding: [50, 30]
            spacing: 40
            MenuItem:
                text: 'Play Endless Mode'
                on_release: root.goto_quiz('endless')
            MenuItem:
                text: 'Play TimeAttack Mode'
                on_release: root.goto_quiz('timeattack')
            MenuItem:
                text: 'View Records'
                on_release: root.goto_records()
            MenuItem:
                text: 'Language Settings'
                on_release: root.goto_language_settings()
            MenuItem:
                text: 'Credits'
                on_release: root.goto_credits()
            MenuItem:
                text: 'Back to title'
                on_release: root.goto_title()
"""
customwidgets.do_nothing()


class MenuScreen(Screen):

    def __init__(self, *, appglobals, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self._funcs = appglobals.funcs
        self._data = appglobals.data

    def goto_quiz(self, mode):
        self._data.mode = mode
        self._funcs.play_sound('bween')
        self._funcs.switch_screen('countdown', FadeTransition(duration=1))

    def goto_records(self):
        self._funcs.play_sound('bween')
        self._funcs.switch_screen(
            'records',
            transition=FadeTransition(duration=.4)
        )

    def goto_title(self):
        self._funcs.switch_screen(
            'title',
            transition=FadeTransition(duration=.6)
        )

    def goto_credits(self):
        self._funcs.play_sound('bween')
        self._funcs.switch_screen('credits', FadeTransition())

    def goto_language_settings(self):
        self._funcs.play_sound('bween')
        self._funcs.switch_screen('language_settings', FadeTransition())


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = MenuScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
