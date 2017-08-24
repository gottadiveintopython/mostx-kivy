# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

import beforetest
import applicationstate
import scenes.scene_countdown


class TestApp(App):

    def build(self):
        appstate = applicationstate.create_default()
        appstate.data.mode = r'endless'
        self.root = root = ScreenManager()
        root.add_widget(Screen())
        root.add_widget(
            scenes.scene_countdown.instantiate(appstate=appstate)
        )
        return root

    def on_start(self):
        self.root.current = r'countdown'


if __name__ == r'__main__':
    TestApp().run()
