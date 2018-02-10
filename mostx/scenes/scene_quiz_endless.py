# -*- coding: utf-8 -*-

import random

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import (
    NumericProperty, BooleanProperty, StringProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import (
    ScreenManager, Screen, SlideTransition, FadeTransition, NoTransition
)

import quizgenerator
import customwidgets
from attrdict import attrdict

__all__ = [r'instantiate']
KV_CODE = r"""
#:set BUTTON_FILENAME r'menu_button.png'

<QuizButtonLayout>:
    _private_1: (len(self.children) + 1) ** 2
    padding: [self.width / self._private_1, self.height / self._private_1]
    spacing: self.padding[0] if (self.orientation == r'horizontal') else self.padding[1]

<LevelupScreen>:
    AutoLabel:
        text: r'Level'
        halign: r'center'
        valign: r'middle'
        size_hint: 0.6, 0.4
        pos_hint: {r'x':0.1, r'center_y':0.5}
    AutoLabel:
        id: level
        halign: r'center'
        valign: r'middle'
        size_hint: 0.2, 0.5
        pos_hint: {r'x':0.7, r'center_y':0.5}

<QuizScreen>:
    ImageButton:
        size_hint: 0.1, 0.1
        pos_hint: {r'x': 0.01, r'top': 0.99}
        source: BUTTON_FILENAME
        on_press: root.manager.on_button_menu()
    AutoLabel:
        size_hint: 0.2, 0.1
        pos_hint: {r'x': 0.11, r'top': 0.99}
        color: [0.6, 0.6, 1.0, 1]
        text: r'{}/{}'.format(root.num_cleared, root.num_answered)
    ClockLabel:
        size_hint: 0.25, 0.1
        pos_hint: {r'x': 0.7, r'top': 0.99}
        text: r'00:00'
        seconds: root.time
    AutoLabel:
        id: sentence_area
        size_hint: 0.9, 0.68
        pos_hint: {r'x':0.05, r'y':0.18}
        font_name: root.font_name
    QuizButtonLayout:
        id: choosing_area
        size_hint: 1.0, 0.14
        pos_hint: {r'x':0, r'y':0}

<CorrectOrNotScreen>:
    ImageButton:
        size_hint: 0.1, 0.1
        pos_hint: {r'x': 0.01, r'top': 0.99}
        source: BUTTON_FILENAME
        on_press: root.manager.on_button_menu()
    AutoLabel:
        size_hint: 0.2, 0.1
        pos_hint: {r'x': 0.11, r'top': 0.99}
        color: [0.6, 0.6, 1.0, 1]
        text: r'{}/{}'.format(root.num_cleared, root.num_answered)
    ClockLabel:
        size_hint: 0.25, 0.1
        pos_hint: {r'x':0.7, r'top':0.99}
        seconds: root.time
    AutoLabel:
        size_hint: 0.6, 0.5
        pos_hint: {r'x':0.2, r'y':0.25}
        text: r'Correct' if root.is_correct else r'Incorrect'
    RoundedButton:
        size_hint: 0.25, 0.15
        pos_hint: {r'center_x':0.2, r'y':0.05}
        text: r'Lookback'
        on_release: root.on_button_lookback()
    RoundedButton:
        size_hint: 0.25, 0.15
        pos_hint: {r'center_x':0.8, r'y':0.05}
        text: r'Next'
        on_release: root.on_button_next()
    AutoLabel:
        id: l_timeinc
        size_hint: 0.2, 0.08
        pos_hint: {r'x':0.75, r'y':0.8}
        text: (r'+{}s' if root.is_correct else r'-{}s').format(root.time_increament)
        color: [0.8, 0.8, 0.2, 1] if root.is_correct else [0.3, 0.3, 0.8, 1]

<LookbackScreen>:
    AutoLabel:
        size_hint: 0.9, 0.7
        pos_hint: {r'center_x': 0.5, r'y': 0.25}
        text: root.quiz_str
        font_name: root.font_name
        color: [0.5, 0.5, 0.5, 1]
    AutoLabel:
        size_hint: 0.2, 0.2
        pos_hint: {r'center_x': 0.5, r'y': 0.05}
        text: root.correct_answer
        color: [0.8, 0.8, 0.2, 1]
    AutoLabel:
        size_hint: 0.3, 0.2
        pos_hint: {r'x': 0.65, r'y': 0.05}
        text: r'   (^_^)' if root.is_correct else r'...(-_-)'

<Manager>:
"""


class QuizButtonLayout(BoxLayout):
    r'''Quizの選択肢のButtonの配置を行うLayout'''
    _private_1 = NumericProperty()


class LevelupScreen(Screen):

    def __init__(self, *, quizstate, appstate, **kwargs):
        super(LevelupScreen, self).__init__(**kwargs)
        self._quizstate = quizstate
        self._animation_fadeout = Animation(
            opacity=0,
            step=0.1,
            duration=0.2,
            transition=r'in_cubic'
        )
        self._animation_fadeout.bind(on_complete=self.on_fadeout_complete)
        self._animation_fadein = Animation(
            opacity=1,
            step=0.1,
            duration=0.2,
            transition=r'in_cubic'
        )

    def on_fadeout_complete(self, anim, widget):
        widget.text = str(self._quizstate.level + 1)
        self._animation_fadein.start(widget)

    def on_pre_enter(self):
        self.ids.level.text = str(self._quizstate.level)

    def on_enter(self):
        self._animation_fadeout.start(self.ids.level)

    def on_touch_down(self, touch):
        self.manager.switch_screen(r'quiz')
        return True


class QuizScreen(Screen):

    num_cleared = NumericProperty()
    num_answered = NumericProperty()
    time = NumericProperty()
    font_name = StringProperty(r'Roboto')

    def __init__(self, *, quizstate, appstate, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self._quizstate = quizstate
        self._all_buttons = []
        self._show_state = None

    def on_touch_down(self, touch):
        if self._show_state == r'facts':
            choosing_area = self.ids[r'choosing_area']
            sentence_area = self.ids[r'sentence_area']
            sentence_area.text = self._quizstate.quiz.question
            choosing_area.disabled = False
            self._show_state = r'question'
            return True
        else:
            return super(QuizScreen, self).on_touch_down(touch)

    def on_choose(self, button):
        if self._show_state == r'question':
            self.clock_pause()
            self.manager.on_choose(button.text)
            self._show_state = None

    def on_pre_enter(self):
        quizstate = self._quizstate
        self.num_cleared = quizstate.num_cleared
        self.num_answered = quizstate.num_answered
        self.time = quizstate.time
        quiz = quizstate.quiz
        # choosing_area
        num_choices = len(quiz.choices)
        choosing_area = self.ids[r'choosing_area']
        sentence_area = self.ids[r'sentence_area']
        choosing_area.clear_widgets()
        if len(self._all_buttons) < num_choices:
            for i in range(num_choices - len(self._all_buttons)):
                button = customwidgets.RoundedButton()
                button.bind(on_release=self.on_choose)
                self._all_buttons.append(button)
        for (button, choice,) in zip(self._all_buttons, quiz.choices):
            button.text = choice
            choosing_area.add_widget(button)
        # sentence_area
        sentence = '\n'.join(quiz.facts)
        if quizstate.is_show_question_with_facts:
            sentence = '\n'.join((sentence, quiz.question,))
            choosing_area.disabled = False
            self._show_state = r'question'
        else:
            choosing_area.disabled = True
            self._show_state = r'facts'
        sentence_area.text = sentence
        self.clock_resume()

    def on_pre_leave(self):
        self.clock_pause()

    def clock_resume(self):
        Clock.schedule_once(
            lambda dt: Clock.schedule_interval(self.clock_callback, 0.1),
            0
        )

    def clock_pause(self):
        Clock.unschedule(self.clock_callback)

    def clock_callback(self, dt):
        self.time = max(0, self.time - dt)
        if self.time == 0:
            self.manager.on_timeout()
            return False
        return True


class CorrectOrNotScreen(Screen):

    num_cleared = NumericProperty()
    num_answered = NumericProperty()
    time = NumericProperty()
    is_correct = BooleanProperty()
    time_increament = NumericProperty()

    def __init__(self, *, quizstate, appstate, **kwargs):
        super(CorrectOrNotScreen, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._quizstate = quizstate
        self._animation_timeinc = Animation(
            opacity=0,
            step=0.1,
            duration=0.5,
            transition=r'in_cubic'
        )
        self._is_play_animation = False

    def on_pre_enter(self):
        quizstate = self._quizstate
        self.num_answered = quizstate.num_answered
        self.num_cleared = quizstate.num_cleared
        self.time = quizstate.time
        self.is_correct = quizstate.is_correct
        self.time_increament = quizstate.time_increament

    def on_enter(self):
        if self._is_play_animation:
            self._is_play_animation = False
            l_timeinc = self.ids[r'l_timeinc']
            if self.time_increament == 0:
                l_timeinc.opacity = 0
            else:
                l_timeinc.opacity = 1.0
                Clock.schedule_once(
                    lambda dt: self._animation_timeinc.start(l_timeinc),
                    0
                )

    def on_num_answered(self, instance, value):
        if value > 0:
            self._is_play_animation = True

    def on_button_lookback(self):
        self._funcs.play_sound(r'ti')
        self.manager.switch_screen(
            r'lookback',
            transition=SlideTransition(direction=r'right'))

    def on_button_next(self):
        self.manager.next_quiz()


class LookbackScreen(Screen):

    quiz_str = StringProperty()
    correct_answer = StringProperty()
    is_correct = BooleanProperty()
    font_name = StringProperty(r'Roboto')

    def __init__(self, *, quizstate, appstate, **kwargs):
        super(LookbackScreen, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._quizstate = quizstate

    def on_touch_down(self, touch):
        self._funcs.play_sound(r'ti')
        self.manager.switch_screen(
            r'correct_or_not',
            transition=SlideTransition(direction=r'left'))
        return True

    def on_pre_enter(self):
        quizstate = self._quizstate
        quiz = quizstate.quiz
        lines = quiz.facts[:]
        lines.append(quiz.question)
        self.quiz_str = '\n'.join(lines)
        self.correct_answer = quiz.answer
        self.is_correct = quizstate.is_correct


class Manager(ScreenManager):

    def __init__(self, *, appstate, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self._random = random.Random()
        self._funcs = appstate.funcs
        self._data = appstate.data
        self._quizstate = attrdict(
            lang_font_tuples=None,             # list of tuple(language, font_name,)
            level=None,                        # difficulty level
            num_adjectives=None,               # a parameter for quizgenerator.generate_quiz()
            num_choices=None,                  # a parameter for quizgenerator.generate_quiz()
            quiz=None,                         # a quiz returned by quizgenerator.generate_quiz()
            time_increament=None,              # when correct time increase by
            is_show_question_with_facts=None,  # show quiz.question with quiz.facts ?
            num_clear_to_next_level=None,      # number of correct answers to go to next level
            num_cleared=None,                  # number of correct answers
            num_answered=None,                 # number of quizzes you answered
            time=None,                         # time left
            answer=None,                       # your answer of the 'quiz'
            is_correct=None,                   # was your answer collect?
        )
        quizstate = self._quizstate
        self.add_widget(Screen(name=r'blank'))
        for name, klass in {
            r'levelup': LevelupScreen,
            r'lookback': LookbackScreen,
            r'correct_or_not': CorrectOrNotScreen,
            r'quiz': QuizScreen,
        }.items():
            self.add_widget(klass(
                name=name,
                appstate=appstate,
                quizstate=quizstate))

    def switch_screen(self, name, transition=NoTransition()):
        self.transition = transition
        self.current = name

    def update_quiz(self):
        quizstate = self._quizstate
        language, font_name = self._random.choice(quizstate.lang_font_tuples)
        self.get_screen(r'quiz').font_name = font_name
        self.get_screen(r'lookback').font_name = font_name
        quizstate.quiz = quizgenerator.generate_quiz(
            choices=self._quiz_settings[r'choices'][:quizstate.num_choices],
            num_adjectives=quizstate.num_adjectives,
            language=language)

    def goto_result(self, *args):
        quizstate = self._quizstate
        self._data.result = attrdict(
            num_cleared=quizstate.num_cleared,
            num_answered=quizstate.num_answered,
            languages=[lang for lang, font_name in quizstate.lang_font_tuples]
        )
        self._funcs.switch_screen(r'result', FadeTransition(duration=1))

    def on_pre_enter(self):
        quizstate = self._quizstate
        data = self._data
        self._quiz_settings = data.quiz_settings.data[data.mode][
            r'debug' if data.devmode else r'release'
        ]
        quizstate.update(
            lang_font_tuples=[
                (key, value[r'font_name'],) for key, value in
                data.lang_settings.available_languages()
            ],
            level=0,
            num_cleared=0,
            num_answered=0,
            time=self._quiz_settings[r'time'],
            quiz=None,
            answer=None,
            is_correct=None,
        )
        quizstate.update(**self._quiz_settings[r'levels'][0])
        self.update_quiz()
        self.switch_screen(r'blank')

    def on_enter(self):
        self.switch_screen(r'quiz')

    def on_timeout(self):
        self.goto_result()

    def on_choose(self, answer):
        quizstate = self._quizstate
        quizstate.time = self.get_screen(r'quiz').time
        quizstate.answer = answer
        quizstate.is_correct = quizstate.quiz.answer == answer
        quizstate.num_answered += 1
        time_increament = quizstate.time_increament
        if quizstate.is_correct:
            quizstate.num_cleared += 1
            quizstate.time += time_increament
        else:
            quizstate.time = max(0, quizstate.time - time_increament)
        self.switch_screen(r'correct_or_not')
        self._funcs.play_sound(r'correct' if quizstate.is_correct else r'incorrect')

    def next_quiz(self):
        quizstate = self._quizstate
        if quizstate.is_correct and quizstate.num_cleared == quizstate.num_clear_to_next_level:
            quizstate.level += 1
            quizstate.update(**self._quiz_settings[r'levels'][quizstate.level])
            self.update_quiz()
            self.switch_screen(r'levelup', FadeTransition())
        else:
            if quizstate.time == 0:
                self.goto_result()
            else:
                self.update_quiz()
                self.switch_screen(r'quiz')

    def on_button_menu(self):
        popup = customwidgets.YesNoPopup(
            text=r'Go back to the title ?',
            size_hint=(0.6, 0.6,)
        )
        popup.bind(on_yes=self.goto_title)
        popup.open()

    def goto_title(self, *args):
        self.switch_screen(r'blank')
        self._funcs.switch_screen(r'title', FadeTransition())


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    manager = Manager(**kwargs)
    Builder.unload_file(__name__)
    screen = Screen(name=r'quiz_endless')
    screen.add_widget(manager)
    # screenが幾つかのMethod呼び出しをmanagerに任せるよう設定
    for name in r'on_pre_enter on_enter on_pre_leave on_leave'.split():
        def proxy(_name=name):
            func = getattr(manager, _name, None)
            if func is not None:
                func()
        setattr(screen, name, proxy)
    return screen
