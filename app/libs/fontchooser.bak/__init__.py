# -*- coding: utf-8 -*-

from os import listdir as os_listdir
from os.path import join as ospath_join, isfile as ospath_isfile

from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout

__all__ = ('clear_cache', 'FontChooser', )
Builder.load_string(r"""
#:set CLICK_TO_CHOOSE 'click to choose'
#:import DEFAULT_FONT kivy.core.text.DEFAULT_FONT

<FontChooser>:
    BoxLayout:
        orientation: 'vertical'
        padding: 5
        spacing: 5
        BoxLayout:
            padding: 2
            spacing: 2
            size_hint_y: None
            height: '50sp'
            Spinner:
                id: spinner_font_name
                size_hint_x: 5
                text: CLICK_TO_CHOOSE
            Spinner:
                id: spinner_font_size
                size_hint_x: 1
                values: '12 14 16 20 30 40 50 60 70 80 100'.split()
                text: '60'
        TextInput:
            id: textinput
            font_size: int(spinner_font_size.text) if spinner_font_size.text != '' else '30sp'
            font_name:
                DEFAULT_FONT if spinner_font_name.text == CLICK_TO_CHOOSE or spinner_font_name.text == '' \
                else spinner_font_name.text
""")


_fontnames = None
'''Widgetを作る度にフォントファイルを検索するのは嫌なのでこの変数に「フォントファイ
ル名のlist」を保存して置く'''


def _split_dict(dictionary, keys):
    return {
        key: dictionary.pop(key) for key in keys if key in dictionary
    }


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

    def __init__(self, **kwargs):
        delayed_kwargs = _split_dict(kwargs, ('font_name', 'font_size', 'text', ))
        super(FontChooser, self).__init__(**kwargs)
        spinner_font_name = self.ids.spinner_font_name
        spinner_font_size = self.ids.spinner_font_size
        textinput = self.ids.textinput
        spinner_font_name.values.extend(fontnames())
        spinner_font_name.bind(text=self.setter('font_name'))
        spinner_font_size.bind(text=lambda __, value: setattr(self, 'font_size', int(value)))
        textinput.bind(text=self.setter('text'))
        self.bind(font_name=spinner_font_name.setter('text'))
        self.bind(font_size=lambda __, value: setattr(spinner_font_size, 'text', str(value)))
        self.bind(text=textinput.setter('text'))
        for key, value in delayed_kwargs.items():
            setattr(self, key, value)


def _test():
    from kivy.base import runTouchApp
    root = FontChooser(text='FontChooser Test', font_size=80)
    runTouchApp(root)


if __name__ == '__main__':
    _test()
