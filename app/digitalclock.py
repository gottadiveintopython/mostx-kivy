# -*- coding: utf-8 -*-

from kivy.properties import NumericProperty

from flexiblelabel import FlexibleLabel


class DigitalClock(FlexibleLabel):

    seconds = NumericProperty()

    def on_seconds(self, widget, value):
        minutes = int(value // 60)
        seconds = int(value % 60)
        self.text = '{:02}:{:02}'.format(minutes, seconds)
