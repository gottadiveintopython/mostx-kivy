# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, NoTransition

__all__ = (r'instantiate',)
KV_CODE = r"""
<Countdown>:
    seconds: 0
    seconds_int: int(self.seconds)
    text: str(self.seconds_int)
    angle: (1 - (self.seconds % 1.0)) * 360
    canvas.before:
        Color:
            rgb: .1, .1, .1
        Ellipse:
            pos: self.pos
            size: self.size
            segments: 40
            angle_start: 0
            angle_end: self.angle
        Color:
            rgb: .5, .5, .5
        Ellipse:
            pos: self.pos
            size: self.size
            segments: 40
            angle_start: self.angle
            angle_end: 360
    Label:
        text: root.text
        font_size: min(*self.size)
        size_hint: 1, 1
        pos_hint: {r'x': 0, r'y': 0}
<CountdownScreen>:
    name: r'countdown'
    child_width: min(*self.size) * 0.9
    Countdown:
        id: countdown
        size_hint: None, None
        size: root.child_width, root.child_width
        pos_hint: {r'center_x': 0.5, r'center_y': 0.5}
        seconds: root.seconds
"""


class Countdown(FloatLayout):

    seconds = NumericProperty()
    seconds_int = NumericProperty()
    angle = NumericProperty()


class CountdownScreen(Screen):

    seconds = NumericProperty()

    def __init__(self, appstate, **kwargs):
        super(CountdownScreen, self).__init__(**kwargs)
        self._appstate = appstate
        self._bind_id = None

    def on_pre_enter(self):
        self.seconds = 3
        assert self._bind_id is None
        self._bind_id = self.ids.countdown.fbind(r'text', self.on_child_text)

    def on_enter(self):
        # Clock.schedule_once(
        #     (lambda dt: Clock.schedule_interval(self.callback_animate, 0.05)),
        #     0.1
        # )
        Clock.schedule_interval(self.callback_animate, 0.05)

    def on_pre_leave(self):
        assert self._bind_id is not None
        self.ids.countdown.unbind_uid(r'text', self._bind_id)
        self._bind_id = None

    def callback_animate(self, dt):
        self.seconds -= dt
        if self.seconds <= 0:
            self.seconds = 0
            self._appstate.funcs.switch_screen(
                r'quiz_' + self._appstate.data.mode,
                NoTransition()
            )
            return False

    def on_child_text(self, widget, value):
        self._appstate.funcs.play_sound(r'count')


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = CountdownScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
