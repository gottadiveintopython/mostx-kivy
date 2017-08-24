# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, FadeTransition

import quizgenerator
import customwidgets
from .fontchooser import FontChooserPopup

__all__ = [r'instantiate']
KV_CODE = r"""
<LanguageSettingsRow>:
    orientation: r'horizontal'
    padding: 5, 1
    spacing: 2
    language:
    enable: cb_enable.active
    font_name:
    sample_text:
    canvas.before:
        Color:
            rgba: [0.5, 0.2, 0.2, 1]
        Line:
            rectangle: [root.x, root.y, root.width, root.height]
            close: True
    CheckBox:
        id: cb_enable
        active: root.enable
        on_active: root.enable = args[1]
        size_hint_x: 0.1
    Label:
        text: root.language
        font_size: self.height * 0.95
        size_hint_x: 0.4
    Button:
        id: b_choose
        text: r'click to choose font'
        background_color: [0.2, 0.2, 0.2, 1]
        font_size: self.height * 0.9
        size_hint_x: 0.5
        on_release: root.choose_font()

<LanguageSettingsScreen>:
    name: r'language_settings'
    canvas.before:
        Color:
            rgb: 0.5, 0.2, 0.6
        Line:
            points: [10, 0.2 * root.height, root.width - 10, 0.2 * root.height]
            width: 1
    ScrollView:
        size_hint: 0.9, 0.76
        pos_hint: {r'center_x': 0.5, r'y': 0.12}
        GridLayout:
            id: id_layout
            size_hint: 1, None
            height: self.minimum_height
            cols: 1
            row_default_height: 30
            row_force_default: True
            spacing: 30
    RoundedButton:
        size_hint: 0.9, 0.09
        pos_hint: {r'center_x': 0.5, r'center_y': 0.1}
        text: r'Back'
        on_release: root.goto_menu()
"""


class LanguageSettingsRow(BoxLayout):

    language = StringProperty()
    enable = BooleanProperty()
    font_name = StringProperty()
    sample_text = StringProperty()

    def on_font_name(self, instance, value):
        self.ids.b_choose.text = value

    def choose_font(self):
        popup = FontChooserPopup(
            sample_text=self.sample_text,
            font_name=self.font_name)
        popup.bind(font_name=self.setter(r'font_name'))
        popup.open()


class LanguageSettingsScreen(Screen):

    def __init__(self, *, appstate, **kwargs):
        super(LanguageSettingsScreen, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._data = appstate.data
        layout = self.ids.id_layout
        for language, params in self._data.lang_settings.data.items():
            row = LanguageSettingsRow(language=language)
            row.enable = params[r'enable']
            quiz = quizgenerator.generate_quiz(
                language=language,
                choices=r'ABC',
                num_adjectives=2)
            temp = quiz.facts[:]
            temp.append(quiz.question)
            row.sample_text = '\n'.join(temp)
            font_name = params[r'font_name']
            if font_name and font_name != r'':
                row.font_name = font_name
            layout.add_widget(row)

    def apply_settings(self):
        data = self._data.lang_settings.data
        for child in self.ids.id_layout.children:
            data[child.language].update(
                enable=child.enable,
                font_name=child.font_name
            )

    def goto_menu(self):
        funcs = self._funcs
        funcs.play_sound(r'bween')
        num_languages_available = 0
        is_invalid = False
        for child in self.ids.id_layout.children:
            if child.enable:
                if child.font_name == r'':
                    is_invalid = True
                    break
                else:
                    num_languages_available += 1
        if is_invalid or num_languages_available == 0:
            popup = customwidgets.MessagePopup(
                text='Make sure that at least one language is checked.\nAnd all languages you checked are set font.',
                size_hint=(0.9, 0.9,))
            popup.open()
        else:
            self.apply_settings()
            funcs.switch_screen(r'menu', FadeTransition())


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = LanguageSettingsScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
