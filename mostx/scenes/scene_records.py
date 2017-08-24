# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import (
    ScreenManager, Screen, SlideTransition, FadeTransition, NoTransition
)

import customwidgets
from applicationsettings import Records

__all__ = [r'instantiate']
KV_CODE = r"""
#:set LINE_WIDTH 10

<TriangleBase@ButtonBehavior+Widget>:
    points: []
    color: []
    canvas:
        Color:
            rgba: self.color
        Line:
            cap: r'none'
            joint: r'round'
            close: True
            width: LINE_WIDTH
            points: self.points
<TriangleLeft@TriangleBase>:
    points:
        [self.x + LINE_WIDTH, self.y + self.height/2, self.x + self.width - LINE_WIDTH, \
        self.y + LINE_WIDTH, self.x + self.width - LINE_WIDTH, self.y + self.height - LINE_WIDTH]
<TriangleRight@TriangleBase>:
    points:
        [self.x + self.width - LINE_WIDTH, self.y + self.height/2, self.x + LINE_WIDTH, \
        self.y + LINE_WIDTH, self.x + LINE_WIDTH, self.y + self.height - LINE_WIDTH]

<MainScreen>:
    _tcolor: [.2, .6, .2, 1]
    _tw: min(*self.size) / 20
    CustomScreenManager:
        id: label_screenmanager
        size_hint: 0.3, 0.05
        pos_hint: {r'x': 0.01, r'top': 0.99}
    RoundedButton:
        text: r'Back to the Menu'
        size_hint: 0.3, 0.1
        pos_hint: {r'right': 0.98, r'y': 0.03}
        on_release: root.goto_menu()
    RoundedButton:
        text: r'Clear Records'
        size_hint: 0.3, 0.1
        pos_hint: {r'x': 0.02, r'y': 0.03}
        on_release: root.clear_records_after_confirmation()
    TriangleRight:
        color: root._tcolor
        size_hint: None, None
        size: root._tw, root._tw
        pos_hint: {r'right': 0.99, r'center_y': 0.5}
        on_release: root.page_right()
    TriangleLeft:
        color: root._tcolor
        size_hint: None, None
        size: root._tw, root._tw
        pos_hint: {r'x': 0.01, r'center_y': 0.5}
        on_release: root.page_left()
    CustomScreenManager:
        id: record_list_screenmanager
        size_hint: 0.8, 0.7
        pos_hint: {r'center_x': 0.5, r'center_y': 0.5}

<RecordList>:
    ScrollView:
        do_scroll_x: False
        size_hint: 1, 1
        GridLayout:
            id: layout
            size_hint: 1, None
            height: self.minimum_height
            cols: 1
            row_default_height: 50
            row_force_default: True
            padding: [0]
            spacing: 10

<DetailScreen>:
    AutoLabel:
        id: main
        size_hint: 0.9, 0.9
        pos_hint: {r'center_x': 0.5, r'center_y': 0.5}

<Manager>:
"""

MODES = [r'endless', r'timeattack']


def _format_time(time):
    minutes = time // 60
    seconds = time % 60
    return r'{:02}:{:02}'.format(minutes, seconds)


class CustomScreenManager(ScreenManager):

    def switch_screen(self, name, transition=NoTransition()):
        self.transition = transition
        self.current = name


class RecordList(Screen):

    def __init__(self, *, appstate, **kwargs):
        super(RecordList, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._data = appstate.data
        layout = self.ids.layout
        self._buttons = buttons = []
        for i in range(Records.MAX_RECORDS):
            button = customwidgets.BorderedButton()
            button.bind(on_release=self.open_detail)
            buttons.append(button)
            layout.add_widget(button)

    def update(self):
        mode = self.name
        rlist = self._data.records.data[mode]
        if mode == r'timeattack':
            for button, record in zip(self._buttons, rlist):
                button.record = record
                button.text = r'{: >6} pts   {: >10}'.format(
                    record[r'points'],
                    record[r'date']
                )
        elif mode == r'endless':
            for button, record in zip(self._buttons, rlist):
                button.record = record
                button.text = r'{: >6} quizzes   {: >10}'.format(
                    record[r'num_cleared'],
                    record[r'date']
                )
        for i in range(Records.MAX_RECORDS - len(rlist)):
            button = self._buttons[-1 - i]
            button.record = None
            button.text = r'------------'

    def open_detail(self, button):
        record = button.record
        if record is None:
            self._funcs.play_sound(r'ti')
        else:
            self.manager.parent.open_detail(mode=self.name, record=record)


class MainScreen(Screen):

    TCOLOR1 = [.2, .4, .2, 1]
    TCOLOR2 = [.2, .8, .2, 1]
    FREQ_CHANGE_TCOLOR = .6

    def __init__(self, *, appstate, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._data = appstate.data
        self._mode_index = 0
        record_list_screenmanager = self.ids.record_list_screenmanager
        label_screenmanager = self.ids.label_screenmanager
        for mode in MODES:
            record_list = RecordList(name=mode, appstate=appstate)
            record_list_screenmanager.add_widget(record_list)
            screen = Screen(name=mode)
            screen.add_widget(customwidgets.AutoLabel(text=mode))
            label_screenmanager.add_widget(screen)

    def on_pre_enter(self):
        Clock.schedule_once(self.change_to_tcolor1, self.FREQ_CHANGE_TCOLOR)

    def on_leave(self):
        Clock.unschedule(self.change_to_tcolor1)
        Clock.unschedule(self.change_to_tcolor2)

    def update(self):
        for screen in self.ids.record_list_screenmanager.screens:
            screen.update()

    def change_to_tcolor1(self, dt):
        self._tcolor = self.TCOLOR1
        Clock.schedule_once(self.change_to_tcolor2, self.FREQ_CHANGE_TCOLOR)

    def change_to_tcolor2(self, dt):
        self._tcolor = self.TCOLOR2
        Clock.schedule_once(self.change_to_tcolor1, self.FREQ_CHANGE_TCOLOR)

    def page_left(self):
        self._funcs.play_sound(r'ti')
        self._mode_index = (self._mode_index + len(MODES) - 1) % len(MODES)
        self.ids.label_screenmanager.switch_screen(
            MODES[self._mode_index],
            transition=SlideTransition(direction=r'right')
        )
        self.ids.record_list_screenmanager.switch_screen(
            MODES[self._mode_index],
            transition=SlideTransition(direction=r'right')
        )

    def page_right(self):
        self._funcs.play_sound(r'ti')
        self._mode_index = (self._mode_index + 1) % len(MODES)
        self.ids.label_screenmanager.switch_screen(
            MODES[self._mode_index],
            transition=SlideTransition(direction=r'left')
        )
        self.ids.record_list_screenmanager.switch_screen(
            MODES[self._mode_index],
            transition=SlideTransition(direction=r'left')
        )

    def goto_menu(self):
        self.manager.goto_menu()

    def open_detail(self, *, mode, record):
        self._funcs.play_sound(r'bween')
        detail = self.manager.get_screen(r'detail')
        detail.update(mode=mode, record=record)
        self.manager.switch_screen(r'detail', FadeTransition(duration=0.2))

    def clear_records_after_confirmation(self):
        popup = customwidgets.YesNoPopup(
            text='You REALLY want to clear records?\n(Clear both ENDLESS and TIMEATTACK records)',
            size_hint=(0.85, 0.85,)
        )
        popup.bind(on_yes=self.clear_records_and_go_menu)
        popup.open()

    def clear_records_and_go_menu(self, *args):
        self._data.records.clear()
        self.manager.goto_menu()


class DetailScreen(Screen):

    def update(self, *, mode, record):
        self._mode = mode
        if mode == r'timeattack':
            text = r"""{r[date]}
  Points    ... {r[points]}
  Answered  ... {r[num_answered]}
  Correct   ... {r[num_cleared]}
  Ratio     ... {r[num_cleared]}/{r[num_answered]}({ratio:.1f}%)
  Time      ... {formated_time}
  Languages ... {languages}""".format(
                r=record,
                ratio=(record[r'num_cleared'] / record[r'num_answered'] * 100),
                formated_time=_format_time(record[r'time']),
                languages=r', '.join(record[r'languages']))
        elif mode == r'endless':
            text = r"""{r[date]}
  Correct   ... {r[num_cleared]}
  Answered  ... {r[num_answered]}
  Ratio     ... {r[num_cleared]}/{r[num_answered]}({ratio:.1f}%)
  Languages ... {languages}""".format(
                r=record,
                ratio=((record[r'num_cleared'] / record[r'num_answered'] * 100) if record[r'num_answered'] != 0 else 0),
                languages=r', '.join(record[r'languages']))
        self.ids.main.text = text

    def on_touch_down(self, touch):
        self.manager.switch_screen(r'main')
        return True


class Manager(CustomScreenManager):

    def __init__(self, *, appstate, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._data = appstate.data
        self._mode_index = 0
        self.add_widget(Screen(name=r'blank'))
        self.add_widget(MainScreen(name=r'main', appstate=appstate))
        self.add_widget(DetailScreen(name=r'detail'))

    def on_pre_enter(self):
        self.get_screen(r'main').update()
        self.switch_screen(r'blank')

    def on_enter(self):
        self.switch_screen(r'main')

    def goto_menu(self):
        funcs = self._funcs
        funcs.play_sound(r'bween')
        funcs.switch_screen(r'menu', FadeTransition())


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    manager = Manager(**kwargs)
    Builder.unload_file(__name__)
    screen = Screen(name=r'records')
    screen.add_widget(manager)
    # screenが幾つかのMethod呼び出しをmanagerに任せるよう設定
    for name in r'on_pre_enter on_enter on_pre_leave on_leave'.split():
        def proxy(_name=name):
            func = getattr(manager, _name, None)
            if func is not None:
                func()
        setattr(screen, name, proxy)
    return screen

