# -*- coding: utf-8 -*-

import kivy.resources
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, FadeTransition

import customwidgets
from .bouncingsprites import BouncingSprites

__all__ = ('instantiate',)
KV_CODE = r"""
<TitleScreen>:
    name: 'title'
    AutoLabel:
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
customwidgets.do_nothing()


class TitleScreen(Screen):

    def __init__(self, *, appglobals, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        self._appglobals = appglobals
        self._anim_layer = BouncingSprites(
            atlasfilepath=kivy.resources.resource_find('characters.atlas'),
            size=(1000, 1000),
            size_hint=(1, 1)
        )
        self.add_widget(self._anim_layer)

    def on_pre_enter(self):
        self._appglobals.funcs.play_sound('intro')

    def on_enter(self):
        self._anim_layer.start_animation()

    def on_pre_leave(self):
        self._anim_layer.stop_animation()

    def go_menu(self):
        self._appglobals.funcs.play_sound('bween')
        self._appglobals.funcs.switch_screen(
            'menu',
            transition=FadeTransition(duration=.8)
        )

    def switch_devmode(self, button):
        data = self._appglobals.data
        self._appglobals.funcs.play_sound('bween')
        if data.devmode:
            data.devmode = False
            button.text = ''
        else:
            data.devmode = True
            button.text = 'dev'


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = TitleScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
