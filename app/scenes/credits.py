# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.resources import resource_find
from kivy.uix.screenmanager import Screen, FadeTransition
from kivy.properties import ObjectProperty

from flexiblelabel import FlexibleLabel

__all__ = ('instantiate', )


class MostxCreditsScreen(Screen):

    appglobals = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(resource_find('credits.txt'), 'rt', encoding='utf-8') as reader:
            self.add_widget(FlexibleLabel(text=reader.read(), padding=['20sp', '20sp']))

    def on_touch_down(self, touch):
        self.appglobals.funcs.switch_scene('menu', FadeTransition())
        return True


def instantiate(**kwargs):
    return MostxCreditsScreen(**kwargs)
