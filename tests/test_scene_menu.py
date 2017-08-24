# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager

import beforetest
import applicationstate
import scenes.scene_menu


def _test():
    root = ScreenManager()
    root.add_widget(
        scenes.scene_menu.instantiate(
            appstate=applicationstate.create_default()
        )
    )
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
