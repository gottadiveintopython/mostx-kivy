# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.resources import resource_find
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.properties import ObjectProperty

import customwidgets
from .bouncingsprites import MostxTitleBouncingSprites

KV_CODE = r"""
<MostxTitleScreen>:
    name: 'title'
    FlexibleLabel:
        text: '"Mostx"\nQuiz Generator'
        halign: 'center'
        size_hint: 0.9, 0.6
        pos_hint: {'x':0.05, 'y':0.35}
    RoundedButton:
        text: 'Start'
        border_width: 2
        size_hint: 0.4, 0.15
        pos_hint: {'center_x':0.5, 'y':0.1}
        on_release: root.go_menu()
    BorderlessButton:
        size_hint: 0.1, 0.1
        pos_hint: {'x':0, 'y':0.9}
        color: [6, 6, 0, 1]
        on_release: root.switch_devmode(args[0])
"""


class MostxTitleScreen(Screen):

    appglobals = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bouncing = MostxTitleBouncingSprites(
            atlasfilepath=resource_find('image/characters.atlas'),
            size=(1000, 1000),
            size_hint=(1, 1)
        )
        self.add_widget(self._bouncing)

    def on_pre_enter(self):
        self.appglobals.funcs.play_sound('intro')

    def on_enter(self):
        self._bouncing.start_animation()

    def on_pre_leave(self):
        self._bouncing.stop_animation()

    def go_menu(self):
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        funcs.switch_scene(
            'menu',
            transition=FadeTransition(duration=.8)
        )

    def switch_devmode(self, button):
        data = self.appglobals.data
        self.appglobals.funcs.play_sound('bween')
        if data.devmode:
            data.devmode = False
            button.text = ''
        else:
            data.devmode = True
            button.text = 'dev'


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = MostxTitleScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
