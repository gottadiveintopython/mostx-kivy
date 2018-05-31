# -*- coding: utf-8 -*-


__all__ = ('clear_cache', 'FontChooser', )

from os import listdir as os_listdir
from os.path import join as ospath_join, isfile as ospath_isfile

from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout


CLICK_TO_CHOOSE = 'click to choose'

Builder.load_string(r"""
#:import DEFAULT_FONT kivy.core.text.DEFAULT_FONT

<FontChooser>:
    _spinner_font_name: spinner_font_name
    font_size: int(spinner_font_size.text) if spinner_font_size.text else 60
    BoxLayout:
        orientation: 'vertical'
        padding: sp(5)
        spacing: sp(5)
        BoxLayout:
            padding: sp(2)
            spacing: sp(2)
            size_hint_y: None
            height: '50sp'
            Spinner:
                id: spinner_font_name
                size_hint_x: 5
                text: root.font_name or '{}'
            Spinner:
                id: spinner_font_size
                size_hint_x: 1
                values: '12 14 16 20 30 40 50 60 70 80 100'.split()
                text: str(root.font_size)
        TextInput:
            id: textinput
            font_size: root.font_size
            font_name: root.font_name or DEFAULT_FONT
            text: root.text
""".format(CLICK_TO_CHOOSE))


_fontnames = None
'''Widgetを作る度にフォントファイルを検索するのは嫌なのでこの変数に「フォントファイ
ル名のlist」を保存して置く'''


def clear_cache():
    '''保存して置いた「フォントファイル名のlist」を削除'''
    global _fontnames
    _fontnames = None


def fontnames():
    '''フォントファイルを検索しそのiterableを返す'''
    global _fontnames
    if _fontnames is None:
        fontnamesset = set()
        for directory in LabelBase.get_system_fonts_dir():
            for filename in os_listdir(directory):
                if ospath_isfile(ospath_join(directory, filename)):
                    if filename.endswith('.ttf') or filename.endswith('.ttc'):
                        fontnamesset.add(filename)
        _fontnames = list(fontnamesset)
        _fontnames.sort(key=(lambda x: x.lower()))
    return _fontnames


class FontChooser(FloatLayout):

    font_name = StringProperty()
    font_size = NumericProperty()
    text = StringProperty()
    _spinner_font_name = ObjectProperty()

    def on__spinner_font_name(self, __, spinner_font_name):
        def on_text(__, text):
            if text in ('', CLICK_TO_CHOOSE, ):
                pass
            else:
                self.font_name = text
        spinner_font_name.values.extend(fontnames())
        spinner_font_name.bind(text=on_text)


def _test():
    from kivy.base import runTouchApp
    root = FontChooser(text='FontChooser Test')
    runTouchApp(root)


if __name__ == '__main__':
    _test()
