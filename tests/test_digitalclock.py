# -*- coding: utf-8 -*-

import beforetest
from digitalclock import DigitalClock


def _test():
    from kivy.app import App
    from kivy.clock import Clock

    class TestApp(App):

        def build(self):
            self.root = DigitalClock(seconds=0)
            return self.root

        def on_start(self):
            Clock.schedule_interval(self._update_clock, 0.1)

        def _update_clock(self, dt):
            self.root.seconds += dt

    TestApp().run()


if __name__ == '__main__':
    _test()
