# -*- coding: utf-8 -*-

__all__ = ('instantiate', )

from kivy.lang import Builder
from kivy.properties import (
    StringProperty, BooleanProperty, ObjectProperty,
)
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen, FadeTransition

import mostx
from flexiblelabel import FlexibleLabel
import customwidgets
from fontchooser import FontChooser
from popuptemplate.popupwithbuttons import PopupWithButtons


Builder.load_string(r'''
<MostxLangSettingsViewClass>:
    canvas.before:
        Color:
            rgba: [0.5, 0.2, 0.2, 1]
        Line:
            rectangle: [*self.pos, *self.size, ]
    CheckBox:
        active: root.enable
        on_press: root.on_checkbox_pressed(self)
        size_hint_x: 0.1
    FlexibleLabel:
        text: root.lang
        padding: 2, 2,
        size_hint_x: 0.4
    BorderedButton:
        text: root.font_name or 'click to choose font'
        padding: 2, 2,
        size_hint_x: 0.5
        on_release: root.recycleview.choose_font(lang=root.lang)

<MostxLangSettingsScreen>:
    name: 'langsettings'
    BoxLayout:
        orientation: 'vertical'
        padding: '5sp', '5sp'
        MostxLangSettingsRecycleView:
            id: recycleview
            viewclass: 'MostxLangSettingsViewClass'
            RecycleBoxLayout:
                orientation: 'vertical'
                default_size_hint: 1, None
                default_size: None, sp(40)
                size_hint_y: None
                height: self.minimum_height
                padding: sp(5), sp(5),
                spacing: sp(10)
        Widget:
            size_hint_y: 0.02
            canvas:
                Color:
                    rgb: 0.4, 0.2, 0.6
                Line:
                    points: [self.x, self.center_y, self.right, self.center_y, ]
                    width: 2
        FloatLayout:
            size_hint_y: 0.1
            RoundedButton:
                size_hint: 0.5, 0.9
                pos_hint: {'center_x': .5, 'center_y': .5, }
                text: 'Back'
                on_release: root.goto_menu()
''')


class MostxLangSettingsViewClass(Factory.BoxLayout):

    lang = StringProperty()
    enable = BooleanProperty()
    font_name = StringProperty()

    @property
    def recycleview(self):
        return self.parent.parent

    def on_checkbox_pressed(self, checkbox):
        # 不要な処理があるように見えますが、こうしないとCheckBoxの描画と大元のデータ
        # との同期をうまくとってくれない
        recycleview = self.recycleview
        src_data = recycleview.src_data
        enable = not src_data[self.lang]['enable']
        src_data[self.lang]['enable'] = enable
        recycleview.synchronize()
        self.enable = enable


class MostxLangSettingsRecycleView(Factory.RecycleView):

    src_data = ObjectProperty()
    _popup = ObjectProperty()

    def choose_font(self, lang):
        popup = self._popup
        if popup is None:
            self._popup = popup = PopupWithButtons(
                content=FontChooser(),
                button_texts=('OK', 'Cancel', ),
            )
            popup.bind(on_button_press=self._on_popup_button_press)
        fontchooser = popup.content
        fontchooser.font_name = self.src_data[lang]['font_name']
        fontchooser.text = '\n'.join(
            mostx.generate_quiz(lang=lang, n_adjectives=1, choices='ABC').statements
        )
        popup._lang = lang
        popup.open(self)

    def _on_popup_button_press(self, popup, button):
        if button.text == 'OK':
            fontchooser = popup.content
            self.src_data[popup._lang]['font_name'] = fontchooser.font_name
            self.synchronize()

    def synchronize(self):
        self.data = sorted([
            {'lang': lang, **params, }
            for lang, params in self.src_data.items()
        ], key=lambda item: item['lang'])


class MostxLangSettingsScreen(Screen):

    appglobals = ObjectProperty()

    def on_pre_enter(self):
        recycleview = self.ids.recycleview
        recycleview.src_data = self.appglobals.langsettings.data
        recycleview.synchronize()

    def goto_menu(self):
        langsettings = self.appglobals.langsettings
        funcs = self.appglobals.funcs
        funcs.play_sound('bween')
        available_langs = {
            lang: value for lang, value in langsettings.available_langs()}
        condition1 = len(available_langs) > 0
        condition2 = True
        if condition1:
            for value in langsettings.data.values():
                if value['enable'] and not value['font_name']:
                    condition2 = False
                    break
        if condition1 and condition2:
            funcs.switch_scene('menu', FadeTransition())
        else:
            popup = PopupWithButtons(
                content=FlexibleLabel(
                    padding=('10sp', '10sp', ),
                    text='Make sure that at least one language is checked.\n'
                         'And all languagess you checked are set font.',
                ),
                button_texts=('OK', ),
            )
            popup.open()


def instantiate(**kwargs):
    return MostxLangSettingsScreen(**kwargs)
