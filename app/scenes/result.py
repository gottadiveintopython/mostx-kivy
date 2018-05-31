# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

import customwidgets


Builder.load_string(r"""
<MostxResultScreen>:
    BoxLayout:
        padding: sp(10), sp(10)
        spacing: sp(10)
        orientation: 'vertical'
        FlexibleLabel:
            id: l_mode
            size_hint_y: 0.1
            color: [0.5, 0.5, 0.5, 1]
        FlexibleLabel:
            id: l_points
            size_hint_y: 0.3
        FlexibleLabel:
            id: l_other_info
            size_hint_y: 0.28
        FlexibleLabel:
            id: l_nth_place
            size_hint_y: 0.2
            color: [0.8, 0.8, 0.2, 1]
""")


def _format_time(time):
    minutes = time // 60
    seconds = time % 60
    return '{:02}:{:02}'.format(minutes, seconds)


class MostxResultScreen(Screen):

    appglobals = ObjectProperty()
    result = ObjectProperty(rebind=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._color_flag = False

    def on_touch_down(self, touch):
        self.appglobals.funcs.switch_scene('title')
        return True

    def on_pre_enter(self):
        appglobals = self.appglobals
        data = appglobals.data
        funcs = appglobals.funcs
        l_mode = self.ids.l_mode
        l_points = self.ids.l_points
        l_other_info = self.ids.l_other_info
        l_nth_place = self.ids.l_nth_place
        result = data.result
        place = False
        if data.devmode:
            pass
        else:
            place = appglobals.records.add(
                mode=data.mode,
                result=result)
        l_other_info.text = 'Correct answer ratio ... {}/{}({:.1f}%)'.format(
            result.n_cleared,
            result.n_answered,
            (float(result.n_cleared) / result.n_answered * 100) if result.n_answered != 0 else 0)
        if data.mode == 'endless':
            l_mode.text = 'Endless Mode'
            l_points.text = '   {} Quizzes'.format(result.n_cleared)
        elif data.mode == 'timeattack':
            l_mode.text = 'Time Attack Mode'
            l_points.text = '   {:.2f} pts'.format(result.points)
            l_other_info.text += "\nTime ... {}".format(
                _format_time(result.time))
        if data.devmode or place < 0:
            l_nth_place.opacity = 0
        else:
            l_nth_place.opacity = 1
            Clock.schedule_interval(
                self.color_callback,
                1
            )
            if place == 0:
                l_nth_place.text = 'New Record'
                funcs.play_sound('newrecord')
            else:
                if place == 1:
                    l_nth_place.text = '2nd place'
                elif place == 2:
                    l_nth_place.text = '3rd place'
                else:
                    l_nth_place.text = str(place) + 'th place'
                funcs.play_sound('rank-in')

    def on_pre_leave(self):
        Clock.unschedule(self.color_callback)

    def color_callback(self, dt):
        l_nth_place = self.ids.l_nth_place
        if self._color_flag:
            l_nth_place.color = [0.8, 0.8, 0.2, 1]
            self._color_flag = False
        else:
            l_nth_place.color = [0.8, 0.4, 0.4, 1]
            self._color_flag = True


def instantiate(**kwargs):
    return MostxResultScreen(**kwargs)
