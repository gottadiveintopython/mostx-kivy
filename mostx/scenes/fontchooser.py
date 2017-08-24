# -*- coding: utf-8 -*-

import os
import os.path

import kivy
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView

__all__ = [r'clear_cache', r'fontnames', r'FontChooser', r'FontChooserPopup']
kivy.require(r'1.9.1')
Builder.load_string(r"""
#:set CLICK_TO_CHOOSE r'click to choose'
#:import DEFAULT_FONT kivy.core.text.DEFAULT_FONT

<FontChooser>:
    BoxLayout:
        size_hint: 1, 1
        pos_hint: {r'x': 0, r'y': 0}
        pos: 0, 0
        orientation: r'vertical'
        padding: 5
        spacing: 5
        BoxLayout:
            padding: 2
            spacing: 2
            size_hint_y: None
            height: r'50sp'
            Spinner:
                id: spinner_font_name
                size_hint_x: 5
                text: CLICK_TO_CHOOSE
            Spinner:
                id: spinner_font_size
                size_hint_x: 1
                values: [r'12', r'14', r'16', r'20', r'30', r'40', r'50', r'60', r'70', r'80', r'100']
                text: r'60'
            TextInput:
                id: ti_sample
                size_hint_x: 5
        Label:
            canvas.before:
                Color:
                    rgba: .5, .5, .5, 1
                Line:
                    close: True
                    rectangle: [self.x, self.y, self.width, self.height]
            id: l_sample
            font_size: int(spinner_font_size.text) if spinner_font_size.text != r'' else r'30sp'
            font_name:
                DEFAULT_FONT if spinner_font_name.text == CLICK_TO_CHOOSE or spinner_font_name.text == r'' \
                else spinner_font_name.text
            text: ti_sample.text

<FontChooserPopup>
    FloatLayout:
        size_hint: 1, 1
        pos_hint: {r'x': 0, r'y': 0}
        pos: 0, 0
        canvas:
            Color:
                rgba: [0, 0, 0, 1]
            Rectangle:
                pos: self.pos
                size: self.size
        Widget:
            id: dummy
            size_hint: 1, 0.86
            pos_hint: {r'center_x': 0.5, r'top': 0.98}
        Button:
            text: r'OK'
            font_size: r'30sp'
            size_hint: 0.2, 0.1
            pos_hint: {r'x': 0.56, r'y': 0.02}
            on_press: root.on_button_ok()
        Button:
            text: r'Cancel'
            font_size: r'30sp'
            size_hint: 0.2, 0.1
            pos_hint: {r'x': 0.78, r'y': 0.02}
            on_press: root.on_button_cancel()
""")


_fontnames = None  # Widgetを作る度にフォントファイルを検索するのは嫌なのでこの変数に「フォントファイル名のlist」を保存して置く


# def _print_widget_info(widget):
#     print(r'''--------------------------
# size_hint : {w.size_hint}
# pos_hint : {w.pos_hint}
# size : {w.size}
# pos : {w.pos}'''.format(w=widget))


def _split_dict(dictionary, keys):
    result = {}
    for key in keys:
        value = dictionary.pop(key, None)
        if value is not None:
            result[key] = value
    return result


def clear_cache():
    r'''保存して置いた「フォントファイル名のlist」を削除'''
    global _fontnames
    _fontnames = None


def fontnames():
    r'''フォントファイルを検索しそのiteratableを返す'''
    global _fontnames
    if _fontnames is None:
        fontnamesset = set()
        for directory in LabelBase.get_system_fonts_dir():
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    if filename.endswith(r'.ttf') or filename.endswith(r'.ttc'):
                        fontnamesset.add(filename)
        _fontnames = list(fontnamesset)
        _fontnames.sort(key=(lambda x: x.lower()))
    return _fontnames


class FontChooser(FloatLayout):

    font_name = StringProperty()
    sample_text = StringProperty()

    def __init__(self, **kwargs):
        delayed_kwargs = _split_dict(kwargs, [r'font_name', r'sample_text'])
        super(FontChooser, self).__init__(**kwargs)
        spinner_font_name = self.ids.spinner_font_name
        spinner_font_name.values.extend(fontnames())
        spinner_font_name.bind(text=self.setter(r'font_name'))
        self.ids.ti_sample.bind(text=self.setter(r'sample_text'))
        self.bind(font_name=spinner_font_name.setter(r'text'))
        self.bind(sample_text=self.ids.ti_sample.setter(r'text'))
        for key, value in delayed_kwargs.items():
            setattr(self, key, value)


class FontChooserPopup(ModalView):

    font_name = StringProperty()
    sample_text = StringProperty()

    def __init__(self, **kwargs):
        delayed_kwargs = _split_dict(kwargs, [r'font_name', r'sample_text'])
        super(FontChooserPopup, self).__init__(**kwargs)
        # dummyをfontchooserに置き換える
        self._fontchooser = fontchooser = FontChooser()
        dummy = self.ids.dummy
        fontchooser.size_hint = dummy.size_hint
        fontchooser.pos_hint = dummy.pos_hint
        parent = dummy.parent
        parent.remove_widget(dummy)
        parent.add_widget(fontchooser)
        #
        fontchooser.bind(sample_text=self.setter(r'sample_text'))
        self.bind(font_name=fontchooser.setter(r'font_name'))
        self.bind(sample_text=fontchooser.setter(r'sample_text'))
        for key, value in delayed_kwargs.items():
            setattr(self, key, value)

    def on_button_ok(self):
        font_name = self._fontchooser.font_name
        if font_name != r'':
            self.font_name = font_name
        self.dismiss()

    def on_button_cancel(self):
        self.dismiss()


def _test():
    from kivy.uix.label import Label
    from kivy.base import runTouchApp
    root = Label(text=r'click to choose font', font_size=20)
    popup = FontChooserPopup(sample_text='珍珠奶茶\nあいうえお\nABCDE')
    root.bind(on_touch_down=popup.open)
    popup.bind(font_name=(lambda ed, value: print(value)))
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
