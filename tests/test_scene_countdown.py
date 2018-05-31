# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

import beforetest
from appglobals import AppGlobals
import scenes.countdown


class TestApp(App):

    def build(self):
        appglobals = AppGlobals()
        appglobals.data.mode = 'endless'
        self.root = root = ScreenManager()
        root.add_widget(Screen())
        root.add_widget(
            scenes.countdown.instantiate(appglobals=appglobals)
        )
        return root

    def on_start(self):
        self.root.current = 'countdown'


if __name__ == '__main__':
    TestApp().run()
