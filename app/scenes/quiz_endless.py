# -*- coding: utf-8 -*-

import random

from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import (
    NumericProperty, BooleanProperty, StringProperty, ObjectProperty,
    ListProperty, OptionProperty,
)
from kivy.uix.screenmanager import (
    Screen, SlideTransition, FadeTransition,
)

import mostx
import customwidgets
from popuptemplate.popupwithbuttons import PopupWithButtons
from attrdict import attrdict
from digitalclock import DigitalClock
from flexiblelabel import FlexibleLabel
from customscreenmanager import MostxScreenManager

__all__ = ('instantiate', )

Builder.load_string('''
<MostxQuizEndlessChoice@RoundedButton>:
    on_press: self.parent.root.on_choose(self.text)
''')

KV_CODE = r'''
#:set CHOICES 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

<MostxQuizLevelup>:
    FlexibleLabel:
        text: 'Level'
        size_hint: 0.6, 0.4
        pos_hint: {'x':0.1, 'center_y':0.5}
    FlexibleLabel:
        id: level
        text: str(root.quizstate.level + 1)
        size_hint: 0.2, 0.5
        pos_hint: {'x':0.7, 'center_y':0.5}

<MostxQuizMain>:
    BoxLayout:
        orientation: 'vertical'
        padding: sp(5), sp(5)
        spacing: sp(5)
        FlexibleLabel:
            font_name: root.font_name
            text:
                '\n'.join(root.quizstate.quiz.statements) if root.show_state == 'all' else (
                '\n'.join(root.quizstate.quiz.statements[:-1]) if root.show_state == 'exclude_question' else (
                root.quizstate.quiz.statements[-1] if root.show_state == 'question' else ''
                ))
        RecycleView:
            data: ({'text': v, } for v in CHOICES[:root.quizstate.n_choices])
            size_hint_y: 0.2
            do_scroll_x: False
            do_scroll_y: False
            viewclass: 'MostxQuizEndlessChoice'
            disabled: not root.show_state in ('all', 'question', )
            RecycleBoxLayout:
                root: root
                padding: sp(20), sp(5)
                spacing: sp(20)
                default_size_hint: 1, 1

<MostxQuizCorrectOrNot>:
    FlexibleLabel:
        size_hint: 0.6, 0.5
        pos_hint: {'x':0.2, 'y':0.25}
        text: 'Correct' if root.quizstate.is_correct else 'Incorrect'
    RoundedButton:
        size_hint: 0.25, 0.15
        pos_hint: {'center_x':0.2, 'y':0.05}
        text: 'Lookback'
        on_release: root.on_button_lookback()
    RoundedButton:
        size_hint: 0.25, 0.15
        pos_hint: {'center_x':0.8, 'y':0.05}
        text: 'Next'
        on_release: root.on_button_next()
    FlexibleLabel:
        id: l_timeinc
        size_hint: 0.2, 0.08
        pos_hint: {'x':0.75, 'y':0.8}
        text: ('+{}s' if root.quizstate.is_correct else '-{}s').format(root.quizstate.time_increament)
        color: [0.8, 0.8, 0.2, 1] if root.quizstate.is_correct else [0.3, 0.3, 0.8, 1]

<MostxQuizLookbackScreen>:
    FlexibleLabel:
        size_hint: 0.9, 0.7
        pos_hint: {'center_x': 0.5, 'y': 0.25}
        text: '\n'.join(root.quizstate.quiz.statements)
        font_name: root.font_name
        color: [0.5, 0.5, 0.5, 1]
    FlexibleLabel:
        size_hint: 0.2, 0.2
        pos_hint: {'center_x': 0.5, 'y': 0.05}
        text: root.quizstate.quiz.answer
        color: [0.8, 0.8, 0.2, 1]
    FlexibleLabel:
        size_hint: 0.3, 0.2
        pos_hint: {'x': 0.65, 'y': 0.05}
        text: '   (^_^)' if root.quizstate.is_correct else '...(-_-)'

<MostxQuizRoot>:
    inner_manager: inner_manager
    BoxLayout:
        orientation: 'vertical'
        padding: sp(5), sp(5),
        spacing: sp(5)
        BoxLayout:
            size_hint_y: 0.1
            ImageButton:
                size_hint_x: 0.1
                source: 'image/menu_button.png'
                on_press: root.on_button_menu()
            FlexibleLabel:
                size_hint_x: 0.2
                color: [0.6, 0.6, 1.0, 1]
                text: '{}/{}'.format(root.quizstate.n_cleared, root.quizstate.n_answered)
            AnchorLayout:
                size_hint_x: 0.8
                anchor_x: 'right'
                DigitalClock:
                    width: self.parent.width * 0.3
                    size_hint_x: None
                    seconds: root.quizstate.time
        MostxScreenManager:
            id: inner_manager
'''


class QuizState(EventDispatcher):
    lang_font_tuples = ListProperty()                # Quizに利用する言語とその言語の表示に用いるFontのtupleのlist [(lang, font_name, ), (lang, font_name, ), ...]
    level = NumericProperty()                        # Quizの難易度
    n_adjectives = NumericProperty()                 # Quizの一文あたりに利用する形容詞の数
    n_choices = NumericProperty()                    # Quizの答えの選択肢の数
    time_increament = NumericProperty()              # Quizに正解した時の残り時間の増加量(かつ間違えた時の減少量)
    show_all_statements_at_once = BooleanProperty()  # Quizの質問文(最も○いのは?)とそれ以外の文(AはBより○○)を同時に表示するか否か
    n_clear_to_go_to_next_level = NumericProperty()  # 次のLevelに進むために必要な総正解数
    n_cleared = NumericProperty()                    # 現在の正解数
    n_answered = NumericProperty()                   # 現在の回答数
    time = NumericProperty()                         # 残り時間
    answer = StringProperty()                        # 現在のQuizへの回答
    is_correct = BooleanProperty()                   # `answer`が正解しているか否か
    quiz = ObjectProperty(                           # 現在のQuiz
        mostx.generate_quiz(choices='AB', lang='english', n_adjectives=1),
        rebind=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MostxQuizLevelup(Screen):

    root = ObjectProperty()
    appglobals = ObjectProperty()
    quizstate = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._anim1 = anim1 = Animation(
            opacity=0,
            duration=0.2,
            transition='in_cubic',
        )
        self._anim2 = Animation(
            opacity=1,
            duration=0.2,
            transition='in_cubic'
        )
        anim1.bind(on_complete=self._on_anim1_complete)

    def _on_anim1_complete(self, *args):
        self.quizstate.level += 1
        self.root.update_quizsettings()
        self._anim2.start(self.ids.level)

    def on_enter(self):
        self._anim1.start(self.ids.level)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self._anim1.have_properties_to_animate(self.ids.level):
                self.manager.switch_screen('main')
                return True
        return super().on_touch_down(touch)


class MostxQuizMain(Screen):

    root = ObjectProperty()
    appglobals = ObjectProperty()
    quizstate = ObjectProperty()
    font_name = StringProperty('Roboto')
    show_state = OptionProperty(
        'None', options=('None', 'all', 'question', 'exclude_question', ))

    _clock_event = None  # Instance属性の既定値として使っている

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.show_state == 'exclude_question':
                self.show_state = 'question'
                return True
        return super().on_touch_down(touch)

    def on_choose(self, answer):
        assert self.show_state in ('question', 'all', )
        self.clock_pause()
        quizstate = self.quizstate
        quizstate.answer = answer
        quizstate.is_correct = quizstate.quiz.answer == answer
        quizstate.n_answered += 1
        time_increament = quizstate.time_increament
        if quizstate.is_correct:
            quizstate.n_cleared += 1
            quizstate.time += time_increament
        else:
            quizstate.time = max(0, quizstate.time - time_increament)
        self.manager.switch_screen('correct_or_not')
        self.appglobals.funcs.play_sound('correct' if quizstate.is_correct else 'incorrect')

    def on_pre_enter(self):
        self.root.update_quiz()
        if self.quizstate.show_all_statements_at_once:
            self.show_state = 'all'
        else:
            self.show_state = 'exclude_question'

    def on_enter(self):
        self.clock_resume()

    def on_pre_leave(self):
        self.clock_pause()

    def clock_resume(self):
        if self._clock_event is not None:
            return
        self._clock_event = Clock.schedule_interval(self._clock_callback, 0.1)

    def clock_pause(self):
        if self._clock_event is None:
            return
        self._clock_event.cancel()
        self._clock_event = None

    def _clock_callback(self, dt):
        quizstate = self.quizstate
        quizstate.time = max(0, quizstate.time - dt)
        if quizstate.time == 0:
            self.root.goto_result()


class MostxQuizCorrectOrNot(Screen):

    root = ObjectProperty()
    appglobals = ObjectProperty()
    quizstate = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._animation = Animation(
            opacity=0,
            duration=0.5,
            transition='in_cubic'
        )
        self._do_play_animation = False
        self.quizstate.bind(n_answered=self.on_n_answered)

    def on_enter(self):
        if self._do_play_animation:
            self._do_play_animation = False
            l_timeinc = self.ids.l_timeinc
            if self.quizstate.time_increament == 0:
                l_timeinc.opacity = 0
            else:
                l_timeinc.opacity = 1.0
                Clock.schedule_once(
                    lambda dt: self._animation.start(l_timeinc),
                    0
                )

    def on_n_answered(self, __, value):
        if value > 0:
            self._do_play_animation = True

    def on_button_lookback(self):
        self.appglobals.funcs.play_sound('ti')
        self.manager.switch_screen(
            'lookback',
            transition=SlideTransition(direction='right'))

    def on_button_next(self):
        quizstate = self.quizstate
        if quizstate.is_correct and quizstate.n_cleared == quizstate.n_clear_to_go_to_next_level:
            self.manager.switch_screen('levelup', FadeTransition())
        else:
            if quizstate.time == 0:
                self.root.goto_result()
            else:
                self.manager.switch_screen('main')


class MostxQuizLookbackScreen(Screen):

    root = ObjectProperty()
    appglobals = ObjectProperty()
    quizstate = ObjectProperty()
    font_name = StringProperty('Roboto')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.appglobals.funcs.play_sound('ti')
            self.manager.switch_screen(
                'correct_or_not',
                transition=SlideTransition(direction='left'))
            return True
        return super().on_touch_down(touch)


class MostxQuizRoot(Screen):

    appglobals = ObjectProperty()
    quizstate = ObjectProperty(QuizState())
    inner_manager = ObjectProperty()
    CHOICES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # これを変更する際はKV側のCHOICESも

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._random = random.Random()
        inner_manager = self.inner_manager
        self.switch_screen = inner_manager.switch_screen
        inner_manager.add_widget(Screen(name='blank'))
        for name, klass in {
            'levelup': MostxQuizLevelup,
            'lookback': MostxQuizLookbackScreen,
            'correct_or_not': MostxQuizCorrectOrNot,
            'main': MostxQuizMain,
        }.items():
            inner_manager.add_widget(klass(
                name=name,
                root=self,
                appglobals=self.appglobals,
                quizstate=self.quizstate))

    def update_quiz(self):
        inner_manager = self.inner_manager
        quizstate = self.quizstate
        lang, font_name = self._random.choice(quizstate.lang_font_tuples)
        inner_manager.get_screen('main').font_name = font_name
        inner_manager.get_screen('lookback').font_name = font_name
        quizstate.quiz = mostx.generate_quiz(
            choices=self.CHOICES[:quizstate.n_choices],
            n_adjectives=quizstate.n_adjectives,
            lang=lang)

    def update_quizsettings(self):
        quizstate = self.quizstate
        quizstate.update(**self._quiz_settings['levels'][quizstate.level])

    def goto_result(self, *args):
        quizstate = self.quizstate
        self.appglobals.data.result = attrdict(
            n_cleared=quizstate.n_cleared,
            n_answered=quizstate.n_answered,
            langs=[lang for lang, font_name in quizstate.lang_font_tuples]
        )
        self.appglobals.funcs.switch_scene('result', FadeTransition(duration=1))

    def on_pre_enter(self):
        quizstate = self.quizstate
        appglobals = self.appglobals
        data = self.appglobals.data
        self._quiz_settings = appglobals.quizsettings.data[data.mode][
            'debug' if data.devmode else 'release'
        ]
        quizstate.update(
            lang_font_tuples=[
                (key, value['font_name'],) for key, value in
                appglobals.langsettings.available_langs()
            ],
            level=0,
            n_cleared=0,
            n_answered=0,
            time=self._quiz_settings['time'],
            is_correct=False,
        )
        self.update_quizsettings()

    def on_enter(self):
        self.switch_screen('main')

    def on_leave(self):
        self.switch_screen('blank')

    def on_button_menu(self):
        play_sound = self.appglobals.funcs.play_sound

        def on_button_press(__, button):
            if button.text == 'Yes':
                self.goto_title()
                play_sound('bween')
            else:
                play_sound('ti')
        popup = PopupWithButtons(
            size_hint=(0.9, 0.9, ),
            button_texts=('Yes', 'No', ),
            content=FlexibleLabel(text='Go back to the title ?'),
            button_class=customwidgets.BorderedButton,
        )
        popup.bind(on_button_press=on_button_press)
        popup.open()
        play_sound('bween')

    def goto_title(self, *args):
        self.appglobals.funcs.switch_scene('title', FadeTransition())


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = MostxQuizRoot(**kwargs)
    Builder.unload_file(__name__)
    return screen
