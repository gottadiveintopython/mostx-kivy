# -*- coding: utf-8 -*-

import itertools
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.screenmanager import (
    ScreenManager, Screen, SlideTransition, FadeTransition, NoTransition
)
from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, StringProperty,
)

import customwidgets
from flexiblelabel import FlexibleLabel
from popuptemplate.popupwithbuttons import PopupWithButtons
from customscreenmanager import MostxScreenManager
# from applicationsettings import Records

__all__ = ('instantiate', )
Builder.load_string(r'''
#:set VIEWCLASSES {'endless': 'MostxRecordsListItemEndless', 'timeattack': 'MostxRecordsListItemTimeattack', '': 'Widget', }

<MostxRecordsListItemEndless>:
    text: '{}  -  {}quizzes'.format(self.date, self.n_cleared)

<MostxRecordsListItemTimeattack>:
    text: '{}  -  {:.2f} points'.format(self.date, self.points)

<MostxRecordsList@Screen>:
    RecycleView:
        id: recycleview
        viewclass: VIEWCLASSES[root.name]
        RecycleBoxLayout:
            orientation: 'vertical'
            default_size: None, sp(50)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height

<MostxRecordsButton@ButtonBehavior+Widget>:
<MostxRecordsRoot>:
    BoxLayout:
        orientation: 'vertical'
        spacing: sp(4)
        FlexibleLabel:
            size_hint_y: 0.1
            text: 'Records'
            outline_color: .3, .3, 1, 0
            outline_width: 2
        BoxLayout:
            spacing: sp(4)
            AnchorLayout:
                size_hint_x: 0.05
                anchor_x: 'center'
                anchor_y: 'center'
                MostxRecordsButton:
                    width: self.parent.width
                    height: self.width
                    size_hint: None, None
                    on_press: root.on_press_triangle(direction='left')
                    canvas:
                        Color:
                            rgb: root.TRIANGLE_COLORS[root._index_of_triangle_color]
                        Triangle:
                            points:
                                (
                                self.x, self.center_y,
                                self.right, self.y,
                                self.right, self.top,
                                )
            BoxLayout:
                orientation: 'vertical'
                FlexibleLabel:
                    text: inner_manager.current
                    size_hint_y: 0.08
                MostxScreenManager:
                    id: inner_manager
                    Screen:
                        name: 'blank'
                    MostxRecordsList:
                        name: 'endless'
                    MostxRecordsList:
                        name: 'timeattack'
            AnchorLayout:
                size_hint_x: 0.05
                anchor_x: 'center'
                anchor_y: 'center'
                MostxRecordsButton:
                    width: self.parent.width
                    height: self.width
                    size_hint: None, None
                    on_press: root.on_press_triangle(direction='right')
                    canvas:
                        Color:
                            rgb: root.TRIANGLE_COLORS[root._index_of_triangle_color]
                        Triangle:
                            points:
                                (
                                self.right, self.center_y,
                                self.x, self.y,
                                self.x, self.top,
                                )
        BoxLayout:
            size_hint_y: 0.1
            padding: sp(40), sp(4)
            spacing: sp(50)
            RoundedButton:
                text: 'Back to the Menu'
                on_release: root.goto_menu()
            RoundedButton:
                text: 'Clear Records'
                on_release: root.clear_records_after_confirmation()
''')


def _format_time(time):
    minutes = int(time // 60)
    seconds = int(time % 60)
    return '{:02}:{:02}'.format(minutes, seconds)


class MostxRecordsListItemEndless(Factory.BorderedButton):
    date = StringProperty()
    n_cleared = NumericProperty()
    n_answered = NumericProperty()
    langs = ListProperty()

    def on_press(self):
        n_answered = self.n_answered
        ratio = 0 if n_answered == 0 else self.n_cleared / n_answered * 100
        text = \
            '{s.date}\n' \
            '  Correct  ...  [color=ffff00]{s.n_cleared}[/color]\n' \
            '  Answered  ...  {s.n_answered}\n' \
            '  Ratio  ...  {s.n_cleared}/{s.n_answered}({ratio:.1f}%)\n' \
            '  Languages  ...  {langs}'.format(
                s=self,
                ratio=ratio,
                langs=', '.join(self.langs))
        modalview = Factory.ModalView()
        modalview.add_widget(
            FlexibleLabel(text=text, size_hint=(0.9, 0.9, ), markup=True))
        modalview.bind(on_touch_down=lambda modalview, __: modalview.dismiss())
        modalview.open()


class MostxRecordsListItemTimeattack(Factory.BorderedButton):
    date = StringProperty()
    points = NumericProperty()
    n_cleared = NumericProperty()
    n_answered = NumericProperty()
    time = NumericProperty()
    langs = ListProperty()

    def on_press(self):
        text = \
            '{s.date}\n' \
            '  Points  ...  [color=ffff00]{s.points}[/color]\n' \
            '  Correct  ...  {s.n_cleared}\n' \
            '  Answered  ...  {s.n_answered}\n' \
            '  Ratio  ...  {s.n_cleared}/{s.n_answered}({ratio:.1f}%)\n' \
            '  Time  ...  {time}\n' \
            '  Languages  ...  {langs}'.format(
                s=self,
                ratio=(self.n_cleared / self.n_answered * 100),
                time=_format_time(self.time),
                langs=', '.join(self.langs))
        modalview = Factory.ModalView()
        modalview.add_widget(
            FlexibleLabel(text=text, size_hint=(0.9, 0.9, ), markup=True))
        modalview.bind(on_touch_down=lambda modalview, __: modalview.dismiss())
        modalview.open()


class MostxRecordsRoot(Factory.Screen):

    appglobals = ObjectProperty()
    TRIANGLE_COLORS = ((.2, .4, .2, ), (.2, .8, .2, ), )
    _index_of_triangle_color = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._screennames = itertools.cycle(('endless', 'timeattack', ))

    def on_pre_enter(self):
        inner_manager = self.ids.inner_manager
        data = self.appglobals.records.data
        inner_manager.get_screen('timeattack').ids.recycleview.data = data['timeattack']
        inner_manager.get_screen('endless').ids.recycleview.data = data['endless']
        inner_manager.switch_screen(next(self._screennames))

    def on_enter(self):
        Clock.schedule_interval(self._update_index_of_triangle_color, 0.6)

    def on_leave(self):
        Clock.unschedule(self._update_index_of_triangle_color)
        inner_manager = self.ids.inner_manager
        inner_manager.switch_screen('blank')

    def _update_index_of_triangle_color(self, __):
        self._index_of_triangle_color = \
            (self._index_of_triangle_color + 1) % len(self.TRIANGLE_COLORS)

    def goto_menu(self):
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        funcs.switch_scene('menu', FadeTransition())

    def clear_records_after_confirmation(self):
        popup = PopupWithButtons(
            button_class=customwidgets.RoundedButton,
            size_hint=(0.85, 0.85, ),
            button_texts=('OK', 'Cancel', ),
            content=FlexibleLabel(
                text='You REALLY want to clear records?\n'
                     '(Clear both ENDLESS and TIMEATTACK records)'),
        )
        popup.bind(on_button_press=self._on_popup_button_press)
        popup.open()

    def _on_popup_button_press(self, popup, button):
        if button.text == 'OK':
            self.appglobals.records.reset()
            self.goto_menu()

    def on_press_triangle(self, direction):
        self.appglobals.funcs.play_sound('ti')
        self.ids.inner_manager.switch_screen(
            next(self._screennames),
            transition=SlideTransition(direction=direction)
        )


def instantiate(**kwargs):
    return MostxRecordsRoot(**kwargs)
