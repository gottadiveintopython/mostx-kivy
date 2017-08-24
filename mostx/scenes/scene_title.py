# -*- coding: utf-8 -*-

import kivy.resources
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, FadeTransition

import customwidgets
from .bouncingsprites import BouncingSprites

__all__ = (r'instantiate',)
KV_CODE = r"""
<TitleScreen>:
    name: r'title'
    AutoLabel:
        text: '"Mostx"\nQuiz Generator'
        halign: r'center'
        size_hint: 0.9, 0.6
        pos_hint: {r'x':0.05, r'y':0.35}
    RoundedButton:
        text: r'Start'
        border_width: 2
        size_hint: 0.4, 0.15
        pos_hint: {r'center_x':0.5, r'y':0.1}
        on_release: root.go_menu()
    BorderlessButton:
        size_hint: 0.1, 0.1
        pos_hint: {r'x':0, r'y':0.9}
        color: [6, 6, 0, 1]
        on_release: root.switch_devmode(args[0])
"""
customwidgets.do_nothing()


class TitleScreen(Screen):

    def __init__(self, *, appstate, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        self._appstate = appstate
        self._anim_layer = BouncingSprites(
            atlasfilepath=kivy.resources.resource_find(r'characters.atlas'),
            size=(1000, 1000),
            size_hint=(1, 1)
        )
        self.add_widget(self._anim_layer)

    def on_pre_enter(self):
        self._appstate.funcs.play_sound(r'intro')

    def on_enter(self):
        self._anim_layer.start_animation()

    def on_pre_leave(self):
        self._anim_layer.stop_animation()

    def go_menu(self):
        self._appstate.funcs.play_sound(r'bween')
        self._appstate.funcs.switch_screen(
            r'menu',
            transition=FadeTransition(duration=.8)
        )

    def switch_devmode(self, button):
        data = self._appstate.data
        self._appstate.funcs.play_sound(r'bween')
        if data.devmode:
            data.devmode = False
            button.text = r''
        else:
            data.devmode = True
            button.text = r'dev'


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = TitleScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
