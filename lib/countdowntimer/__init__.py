# -*- coding: utf-8 -*-
# https://github.com/gottadiveintopython/kivy-module-collection

from pathlib import PurePath
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout

__all__ = ('CountdownTimer', )

PARENT_DIRECTORY = PurePath(__file__).parent

Builder.load_string(r"""
<CountdownTimer>:
    displayed_seconds: int(self.seconds)
    _angle: (1.0 - (self.seconds % 1.0)) * 360
    canvas.before:
        Color:
            rgb: .1, .1, .1
        Ellipse:
            pos: self.pos
            size: self.size
            segments: 40
            angle_start: 0
            angle_end: self._angle
        Color:
            rgb: .5, .5, .5
        Ellipse:
            pos: self.pos
            size: self.size
            segments: 40
            angle_start: self._angle
            angle_end: 360
    Label:
        text: str(root.displayed_seconds)
        font_size: min(*self.size)
        pos_hint: {'x': 0, 'y': 0, }
""")


class CountdownTimer(FloatLayout):

    __events__ = ('on_start', 'on_complete', 'on_cancel', )
    seconds = NumericProperty()
    displayed_seconds = NumericProperty()
    _angle = NumericProperty()

    _clock_event = None
    _sound = SoundLoader.load(
        str(PARENT_DIRECTORY / 'se_maoudamashii_system13.ogg'))

    @property
    def has_started(self):
        return self._clock_event is not None

    def on_displayed_seconds(self, __, value):
        if not self.has_started:
            return
        self._play_sound()

    def _play_sound(self):
        sound = self._sound
        if sound.state == 'play':
            sound.stop()
        sound.play()

    def start(self, seconds):
        if self.has_started:
            self.cancel()
        self.seconds = seconds
        self._clock_event = Clock.schedule_interval(self._progress, 0.05)
        self.dispatch('on_start')

    def cancel(self):
        if not self.has_started:
            return
        self._clock_event.cancel()
        self._clock_event = None
        self.dispatch('on_cancel')

    def _progress(self, dt):
        self.seconds -= dt
        if self.seconds <= 0:
            self.seconds = 0
            self.dispatch('on_complete')
            self._clock_event = None
            return False

    def on_start(self):
        pass

    def on_cancel(self):
        pass

    def on_complete(self):
        pass


def _test():
    from kivy.app import runTouchApp

    root = CountdownTimer()

    def on_touch_down(__, touch):
        if root.has_started:
            root.cancel()
        else:
            root.start(touch.sx * 4.5)

    root.bind(
        on_touch_down=on_touch_down,
        on_start=lambda widget: print('{:.1f}秒のCountdownが始まりました'.format(widget.seconds)),
        on_cancel=lambda widget: print('Countdownが残り{:.1f}秒で中断されました'.format(widget.seconds)),
        on_complete=lambda widget: print('Countdownが終わりました'),
    )
    runTouchApp(root)


if __name__ == '__main__':
    _test()
