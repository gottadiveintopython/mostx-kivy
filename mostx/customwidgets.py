# -*- coding: utf-8 -*-
r'''
このModuleではアプリケーション内の色んな所から利用されるWidgetを定義している。

----------------------------------------------------------------------------
使い方

import customwidgets

label = customwidgets.Autolabel(text=r'test')
----------------------------------------------------------------------------
Widget一覧

AutoLabel         font_sizeを自動調節してくれるLabel
BorderlessButton  枠が無く、見た目がAutoLabelと一緒のButton
BorderedButton    BorderlessButtonに四角い枠が付いた物
RoundedButton     BorderlessButtonに角の丸い四角の枠が付いた物
ImageButton       文字列が無く画像のみのButton
MessagePopup      簡易にメッセージを表示できるModalView
YesNoPopup        二択の質問を簡易に出せるModalView
ClockLabel        デジタル時計(分と秒を表示)
'''

import kivy
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.properties import (
    NumericProperty, StringProperty
)

kivy.require(r'1.9.1')

__all__ = [
    r'do_nothing', r'AutoLabel', r'BorderlessButton', r'BorderedButton',
    r'RoundedButton', r'ImageButton', r'MessagePopup', r'YesNoPopup',
    r'ClockLabel'
]


Builder.load_string(r"""
#:kivy 1.9.1
#:set BUTTON_NORMAL_BG_COLOR [0, 0, 0, 1]
#:set BUTTON_DOWN_BG_COLOR [.2, .2, .2, 1]
#:set LINE_COLOR [.3, .3, .3, 1]


<AutoLabel>:

<BorderlessButton@ButtonBehavior+AutoLabel>:
    adjust_font_size_scaling: 0.95

<BorderedButton>:
    adjust_font_size_scaling: 0.95
    border_width: 1
    canvas.before:
        Color:
            rgba: BUTTON_NORMAL_BG_COLOR if self.state == r'normal' else BUTTON_DOWN_BG_COLOR
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: LINE_COLOR
            #rgba: self.disabled_color if self.disabled else self.color
        Line:
            rectangle: [self.x, self.y, self.width, self.height]
            width: self.border_width

<RoundedButton>:
    adjust_font_size_scaling: 0.95
    border_width: 2
    canvas.before:
        Color:
            rgba: LINE_COLOR
        RoundedRectangle:
            segments: 6
            pos: self.pos
            size: self.size
        Color:
            rgba: BUTTON_NORMAL_BG_COLOR if self.state == r'normal' else BUTTON_DOWN_BG_COLOR
        RoundedRectangle:
            segments: 6
            pos: self.x + self.border_width, self.y + self.border_width
            size: self.width - self.border_width * 2, self.height - self.border_width * 2

<ImageButton@ButtonBehavior+Image>

<MessagePopup>:
    adjust_font_size_scaling: 0.95
    on_touch_up: root.dismiss()
    AutoLabel:
        text: root.text
        size_hint: 0.96, 0.96
        pos_hint: {r'center_x': 0.5, r'center_y': 0.5}

<YesNoPopup>:
    auto_dismiss: False
    BoxLayout:
        orientation: r'vertical'
        padding: 20
        spacing: 20
        AutoLabel:
            size_hint_y: 0.8
            text: root.text
            size_hint: 0.96, 0.88
            pos_hint: {r'center_x': 0.5, r'top': 1}
        BoxLayout:
            size_hint_y: 0.2
            orientation: r'horizontal'
            spacing: 20
            RoundedButton:
                text: root.text_yes
                on_release: root.dispatch(r'on_yes')
            RoundedButton:
                text: root.text_no
                on_release: root.dispatch(r'on_no')

<ClockLabel>:
    seconds: 0
""", filename=__name__)


def do_nothing():
    r'''
この関数は名前通り何もしない。IDEの出す次の類の警告

'customwidgets' imported but unused.

を無くしたい時に使う。
'''
    pass


def _split_dict(dictionary, keys):
    result = {}
    for key in keys:
        value = dictionary.pop(key, None)
        if value is not None:
            result[key] = value
    return result


def _adjust_font_size(label, *, scaling=1.0):
    r"""labelのtextがwidgetの範囲内に収まるようにfont_sizeを調節する関数

    ぴったり収めたい時はscalingに1.0を渡せば良い。
    1.0より大きな値を渡せばwidgetからはみ出し、小さな値なら
    ばその逆である。"""
    texture_width = label.texture_size[0]
    texture_height = label.texture_size[1]
    widget_width = label.width
    widget_height = label.height
    if label.text == r'' or texture_width == 0 or texture_height == 0 or widget_width == 0 or widget_height == 0:
        return
    texture_aspect_ratio = texture_width / texture_height
    widget_aspect_ratio = widget_width / widget_height
    if texture_aspect_ratio < widget_aspect_ratio:
        factor = (widget_height / texture_height) * scaling
    else:
        factor = (widget_width / texture_width) * scaling
    label.font_size = int(factor * label.font_size)


class AutoLabel(Label):
    r'''font_sizeを自動調節するLabel'''

    adjust_font_size_scaling = NumericProperty(1)

    def __init__(self, **kwargs):
        self._need_to_update_texture = False
        self._adjust_font_size_trigger = Clock.create_trigger(
            self._adjust_font_size_callback,
            -1
        )
        super(AutoLabel, self).__init__(**kwargs)

    def on_text(self, __, value):
        self._need_to_update_texture = True
        self._adjust_font_size_trigger()

    def on_size(self, __, value):
        self._adjust_font_size_trigger()

    def _adjust_font_size_callback(self, *args):
        if self._need_to_update_texture:
            self.texture_update()
            self._need_to_update_texture = False
        _adjust_font_size(self, scaling=self.adjust_font_size_scaling)


class BorderedButton(ButtonBehavior, AutoLabel):
    r'''四角い枠付きのButton(font_sizeは自動調節)'''

    border_width = NumericProperty(1)


class RoundedButton(ButtonBehavior, AutoLabel):
    r'''角の丸い枠付きのButton(font_sizeは自動調節)'''
    border_width = NumericProperty(2)


class MessagePopup(ModalView):

    text = StringProperty()


class YesNoPopup(ModalView):

    text = StringProperty()
    text_yes = StringProperty(r'Yes')
    text_no = StringProperty(r'No')

    def __init__(self, **kwargs):
        super(YesNoPopup, self).__init__(**kwargs)
        self.register_event_type(r'on_yes')
        self.register_event_type(r'on_no')

    def on_yes(self):
        self.dismiss()

    def on_no(self):
        self.dismiss()


class ClockLabel(AutoLabel):
    seconds = NumericProperty()

    def on_seconds(self, widget, value):
        minutes = int(value // 60)
        seconds = int(value % 60)
        self.text = r'{:02}:{:02}'.format(minutes, seconds)


BorderlessButton = Factory.BorderlessButton
ImageButton = Factory.ImageButton


def _test():
    from kivy.base import runTouchApp
    yesno_popup = YesNoPopup(text=r'Yes No Popup', size_hint=(0.95, 0.95,))
    yesno_popup.bind(
        on_yes=(lambda *args: print(r'# on_yes')),
        on_no=(lambda *args: print(r'# on_no'))
    )
    msg_popup = MessagePopup(text=r'Message Popup', size_hint=(0.95, 0.95,))
    root = Builder.load_string(r"""
GridLayout:
    cols: 3
    spacing: 10
    padding: 20
    AutoLabel:
        text: r'AutoLabel'
    RoundedButton:
        id: button_yesno_popup
        text: 'RoundButton\n(open YesNoPopup)'
        border_width: 4
    BorderlessButton:
        text: r'BorderlessButton'
        on_press: print(r'BorderlessButton pressed.')
    BorderedButton:
        id: button_msg_popup
        text: 'BorderedButton\n(open MessagePopup)'
        border_width: 2
    ScrollView:
        GridLayout:
            size_hint: 1, None
            height: self.minimum_height
            cols: 1
            row_default_height: 50
            row_force_default: True
            padding: 10
            spacing: 10
            BorderedButton:
                text: r'Apple'
            BorderedButton:
                text: r'Banana'
            BorderedButton:
                text: r'Cucumber'
            BorderedButton:
                text: r'Donut'
            BorderedButton:
                text: r'Eggplant'
            BorderedButton:
                text: r'FurikakeGohan'
    FloatLayout:
        ImageButton:
            pos_hint: {r'center_x': 0.5, r'center_y': 0.5}
            source: r'./data/image/menu_button.png'
            size: self.texture.size
""")
    root.ids.button_yesno_popup.bind(on_release=yesno_popup.open)
    root.ids.button_msg_popup.bind(on_release=msg_popup.open)
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
