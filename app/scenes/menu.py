# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.properties import ObjectProperty

import customwidgets


Builder.load_string(r'''
<MostxMenuItem@BorderedButton>:

<MostxMenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 30]
        spacing: 40
        MostxMenuItem:
            text: 'Play Endless Mode'
            on_release: root.goto_quiz('endless')
        MostxMenuItem:
            text: 'Play TimeAttack Mode'
            on_release: root.goto_quiz('timeattack')
            disabled: True
        MostxMenuItem:
            text: 'View Records'
            on_release: root.goto_records()
        MostxMenuItem:
            text: 'Language Settings'
            on_release: root.goto_langsettings()
        MostxMenuItem:
            text: 'Credits'
            on_release: root.goto_credits()
        MostxMenuItem:
            text: 'Back to title'
            on_release: root.goto_title()
''')


class MostxMenuScreen(Screen):

    appglobals = ObjectProperty()

    def goto_quiz(self, mode):
        self.appglobals.data.mode = mode
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        funcs.switch_scene('countdown', FadeTransition(duration=1))

    def goto_records(self):
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        funcs.switch_scene(
            'records',
            transition=FadeTransition(duration=.4)
        )

    def goto_title(self):
        self.appglobals.funcs.switch_scene(
            'title',
            transition=FadeTransition(duration=.6)
        )

    def goto_credits(self):
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        funcs.switch_scene('credits', FadeTransition())

    def goto_langsettings(self):
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        funcs.switch_scene('langsettings', FadeTransition())


def instantiate(**kwargs):
    return MostxMenuScreen(**kwargs)
