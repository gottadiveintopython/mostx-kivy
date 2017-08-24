# -*- coding: utf-8 -*-


from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

import customwidgets


__all__ = (r'instantiate',)
KV_CODE = r"""
<ResultScreen>:
    name: r'result'
    AutoLabel:
        id: l_mode
        size_hint: 0.4, 0.1
        pos_hint: {r'center_x': 0.5, r'y': 0.85}
        color: [0.5, 0.5, 0.5, 1]
    AutoLabel:
        id: l_points
        size_hint: 0.9, 0.3
        pos_hint: {r'center_x': 0.5, r'y': 0.55}
    AutoLabel:
        id: l_other_info
        size_hint: 0.9, 0.28
        pos_hint: {r'center_x': 0.5, r'y': 0.26}
    AutoLabel:
        id: l_nth_place
        size_hint: 0.5, 0.2
        pos_hint: {r'x': 0.4, r'y': 0.05}
        color: [0.8, 0.8, 0.2, 1]
"""
customwidgets.do_nothing()


def _format_time(time):
    minutes = time // 60
    seconds = time % 60
    return r'{:02}:{:02}'.format(minutes, seconds)


class ResultScreen(Screen):

    def __init__(self, *, appstate, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._data = appstate.data
        self._color_flag = False

    def on_touch_down(self, touch):
        self._funcs.switch_screen(r'title')
        return True

    def on_pre_enter(self):
        data = self._data
        funcs = self._funcs
        l_mode = self.ids.l_mode
        l_points = self.ids.l_points
        l_other_info = self.ids.l_other_info
        l_nth_place = self.ids.l_nth_place
        result = data.result
        place = False
        if data.devmode:
            pass
        else:
            place = data.records.add(
                mode=data.mode,
                result=result.so_to_dict())
        l_other_info.text = r'Correct answer ratio ... {}/{}({:.1f}%)'.format(
            result.num_cleared,
            result.num_answered,
            (float(result.num_cleared) / result.num_answered * 100) if result.num_answered != 0 else 0)
        if data.mode == r'endless':
            l_mode.text = r'Endless Mode'
            l_points.text = r'   {} Quizzes'.format(result.num_cleared)
        elif data.mode == r'timeattack':
            l_mode.text = r'Time Attack Mode'
            l_points.text = r'   {} pts'.format(result.points)
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
                l_nth_place.text = r'New Record'
                funcs.play_sound(r'newrecord')
            else:
                if place == 1:
                    l_nth_place.text = r'2nd place'
                elif place == 2:
                    l_nth_place.text = r'3rd place'
                else:
                    l_nth_place.text = str(place) + r'th place'
                funcs.play_sound(r'rank-in')

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
    Builder.load_string(KV_CODE, filename=__name__)
    screen = ResultScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
