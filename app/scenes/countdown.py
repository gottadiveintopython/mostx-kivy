# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.properties import ObjectProperty


Builder.load_string(r'''
#:import CountdownTimer countdowntimer.CountdownTimer

<MostxCountdownScreen>:
    name: 'countdown'
    countdown: countdown
    CountdownTimer:
        id: countdown
        size_hint: None, None
        size: (min(root.size) * 0.9, ) * 2
        pos_hint: {'center_x': 0.5, 'center_y': 0.5, }
        on_complete: root.on_countdown_complete()
''')


class MostxCountdownScreen(Screen):

    appglobals = ObjectProperty()

    def on_pre_enter(self):
        self.countdown.seconds = 3

    def on_enter(self):
        self.countdown.start(3)

    def on_pre_leave(self):
        self.countdown.cancel()

    def on_countdown_complete(self):
        self.appglobals.funcs.switch_scene(
            'quiz_' + self.appglobals.data.mode,
            NoTransition()
        )


def instantiate(**kwargs):
    return MostxCountdownScreen(**kwargs)
