# -*- coding: utf-8 -*-
'''
このModuleではアプリケーション内の色んな所から利用されるWidgetを定義している。

----------------------------------------------------------------------------
Widget一覧

BorderlessButton  枠が無く、見た目がFlexibleLabelと一緒のButton
BorderedButton    BorderlessButtonに四角い枠が付いた物
RoundedButton     BorderlessButtonに角の丸い四角の枠が付いた物
ImageButton       文字列が無く画像のみのButton
'''

__all__ = (
    'BorderlessButton', 'BorderedButton', 'RoundedButton', 'ImageButton',
)

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty

from flexiblelabel import FlexibleLabel


Builder.load_string(r"""
#:set BUTTON_NORMAL_BG_COLOR [0, 0, 0, 1]
#:set BUTTON_DOWN_BG_COLOR [.2, .2, .2, 1]
#:set LINE_COLOR [.3, .3, .3, 1]


<BorderlessButton@ButtonBehavior+FlexibleLabel>:

<BorderedButton>:
    border_width: 1
    canvas.before:
        Color:
            rgba: BUTTON_NORMAL_BG_COLOR if self.state == 'normal' else BUTTON_DOWN_BG_COLOR
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
    border_width: 2
    canvas.before:
        Color:
            rgba: LINE_COLOR
        RoundedRectangle:
            segments: 6
            pos: self.pos
            size: self.size
        Color:
            rgba: BUTTON_NORMAL_BG_COLOR if self.state == 'normal' else BUTTON_DOWN_BG_COLOR
        RoundedRectangle:
            segments: 6
            pos: self.x + self.border_width, self.y + self.border_width
            size: self.width - self.border_width * 2, self.height - self.border_width * 2

<BorderlessButton, BorderedButton, RoundedButton>:
    padding: ['5sp', '5sp', ]


<ImageButton@ButtonBehavior+Image>
""")


class BorderedButton(ButtonBehavior, FlexibleLabel):
    '''四角い枠付きのButton(font_sizeは自動調節)'''

    border_width = NumericProperty(1)


class RoundedButton(ButtonBehavior, FlexibleLabel):
    '''角の丸い枠付きのButton(font_sizeは自動調節)'''
    border_width = NumericProperty(2)


BorderlessButton = Factory.BorderlessButton
ImageButton = Factory.ImageButton


def _test():
    from kivy.base import runTouchApp
    root = Builder.load_string(r"""
GridLayout:
    cols: 3
    spacing: 10
    padding: '20sp'
    FlexibleLabel:
        text: 'FlexibleLabel'
    RoundedButton:
        text: 'RoundButton'
        border_width: 4
    BorderlessButton:
        text: 'BorderlessButton'
        on_press: print('BorderlessButton pressed.')
    BorderedButton:
        text: 'BorderedButton'
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
                text: 'Apple'
            BorderedButton:
                text: 'Banana'
            BorderedButton:
                text: 'Cucumber'
            BorderedButton:
                text: 'Donut'
            BorderedButton:
                text: 'Eggplant'
            BorderedButton:
                text: 'FurikakeGohan'
    FloatLayout:
        ImageButton:
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            source: 'data/logo/kivy-icon-256.png'
            on_press: print('ImagessButton pressed.')
""")
    runTouchApp(root)


if __name__ == '__main__':
    _test()
