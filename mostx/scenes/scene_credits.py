# -*- coding: utf-8 -*-

import io

import kivy.resources
from kivy.lang import Builder
from kivy.core.text import DEFAULT_FONT
from kivy.uix.screenmanager import Screen, FadeTransition

import customwidgets


__all__ = [r'instantiate']
KV_CODE = r"""
<CreditsScreen>:
    name: r'credits'
    AutoLabel:
        id: id_label
        size_hint: 1, 1
        pos_hint: {r'center_x': 0.5, r'center_y': 0.5}
"""
customwidgets.do_nothing()


class CreditsScreen(Screen):

    def __init__(self, *, appstate, **kwargs):
        super(CreditsScreen, self).__init__(**kwargs)
        self._funcs = appstate.funcs
        self._data = appstate.data

    def on_touch_down(self, touch):
        self._funcs.switch_screen(r'menu', FadeTransition())
        return True

    def on_pre_enter(self):
        # 日本語または中国語のフォントが有効になっている時は
        # credits_kanji.txtを使い、その他の場合はcredits.txtを使う
        lang_font_dict = {
            key: value[r'font_name'] for key, value in
            self._data.lang_settings.available_languages()
        }
        if r'chinese' in lang_font_dict:
            credits_filename = r'credits_kanji.txt'
            font_name = lang_font_dict[r'chinese']
        elif r'japanese' in lang_font_dict:
            credits_filename = r'credits_kanji.txt'
            font_name = lang_font_dict[r'japanese']
        else:
            credits_filename = r'credits.txt'
            font_name = DEFAULT_FONT
        #
        label = self.ids.id_label
        label.font_name = font_name
        with io.open(
            kivy.resources.resource_find(credits_filename),
            r'rt',
            encoding=r'utf-8'
        ) as reader:
            label.text = reader.read()


def instantiate(**kwargs):
    Builder.load_string(KV_CODE, filename=__name__)
    screen = CreditsScreen(**kwargs)
    Builder.unload_file(__name__)
    return screen
