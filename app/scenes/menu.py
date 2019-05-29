# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

import customwidgets


Builder.load_string(r'''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<MostxMenuItem@BorderedButton>:

<MostxMenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 30]
        spacing: 40
        MostxMenuItem:
            text: 'Play Endless Mode'
            on_release:
                root.appglobals.data.mode = 'endless'
                funcs = root.appglobals.funcs
                funcs.play_sound('bween')
                funcs.switch_scene('countdown', FadeTransition(duration=1))
        # MostxMenuItem:
        #     text: 'Play TimeAttack Mode'
        #     on_release:
        #         root.appglobals.data.mode = 'timeattack'
        #         funcs = root.appglobals.funcs
        #         funcs.play_sound('bween')
        #         funcs.switch_scene('countdown', FadeTransition(duration=1))
        #     disabled: True
        MostxMenuItem:
            text: 'View Records'
            on_release:
                funcs = root.appglobals.funcs
                funcs.play_sound('bween')
                funcs.switch_scene(
                'records',
                transition=FadeTransition(duration=.4)
                )
        MostxMenuItem:
            text: 'Language Settings'
            on_release:
                funcs = root.appglobals.funcs
                funcs.play_sound('bween')
                funcs.switch_scene('langsettings', FadeTransition())
        MostxMenuItem:
            text: 'Credits'
            on_release:
                funcs = root.appglobals.funcs
                funcs.play_sound('bween')
                funcs.switch_scene('credits', FadeTransition())
        MostxMenuItem:
            text: 'Back to title'
            on_release:
                root.appglobals.funcs.switch_scene(
                'title',
                transition=FadeTransition(duration=.6),
                )
''')


class MostxMenuScreen(Screen):

    appglobals = ObjectProperty()


def instantiate(**kwargs):
    return MostxMenuScreen(**kwargs)
