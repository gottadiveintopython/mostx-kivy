# -*- coding: utf-8 -*-
# https://github.com/gottadiveintopython/kivy-module-collection

__all__ = ('FlexibleLabel', )

r''':class:`Label` with the ability that automatically adjust :attr:`font_size`
'''

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import BoundedNumericProperty
from kivy.lang import Builder
from kivy.graphics import Rectangle

Builder.load_string(r'''
<-FlexibleLabel>:
    canvas:
        Color:
            rgba: self.color
''')


class FlexibleLabel(Label):

    FL_SCALING_MIN = 0.01
    FL_MAX_SCALING_MIN = 1.2
    FL_MIN_SCALING_MIN = 0.1
    FL_MIN_SCALING_MAX = 0.8

    fl_scaling = BoundedNumericProperty(1, min=FL_SCALING_MIN)
    r''':attr:`texture`が画面に表示される際に幾倍に拡大or縮小されているか。

    This attribute is read-only.

    :attr:`fl_scaling` is a :class:`~kivy.properties.BoundedNumericProperty` and
    defaults to 1.
    '''

    fl_max_scaling = BoundedNumericProperty(FL_MAX_SCALING_MIN, min=FL_MAX_SCALING_MIN)
    r''':attr:`texture`の拡大率の上限。この値を超えそうな時、より大きな
    :attr:`font_size`で:attr:`texture`を作り直す。

    :attr:`fl_max_scaling` is a :class:`~kivy.properties.BoundedNumericProperty`
     and defaults to 2.
    '''

    fl_min_scaling = BoundedNumericProperty(
        FL_MIN_SCALING_MAX, min=FL_MIN_SCALING_MIN, max=FL_MIN_SCALING_MAX)
    r''':attr:`texture`の縮小率の下限。この値を下回りそうな時、より小さな
    :attr:`font_size`で:attr:`texture`を作り直す。

    :attr:`fl_min_scaling` is a :class:`~kivy.properties.BoundedNumericProperty`
     and defaults to 0.5.
    '''

    def __init__(self, **kwargs):
        self._fl_rectangle = None
        self._fl_trigger_update_canvas = Clock.create_trigger(self._fl_update_canvas, -1)
        super(FlexibleLabel, self).__init__(**kwargs)

        def trigger_update_canvas(label, *args):
            label._fl_trigger_update_canvas()
        self.bind(
            texture_size=trigger_update_canvas,
            text=trigger_update_canvas,
            size=trigger_update_canvas,
            pos=trigger_update_canvas,
        )

        # self.canvas.clear()
        # with self.canvas:
        #     color_inst = Color(self.color)
        #     self.bind(color=lambda __, value: setattr(color_inst, 'rgba', value))

    def _fl_update_canvas(self, *args):
        canvas = self.canvas
        rectangle = self._fl_rectangle
        font_size = self.font_size
        # remove previous one
        if rectangle is not None:
            canvas.remove(rectangle)
            self._fl_rectangle = None
        # create new one
        pos, size, scaling = _calculate_pos_and_size_and_scaling(
            self.size, self.texture_size)
        if not (self.fl_min_scaling <= scaling <= self.fl_max_scaling):
            new_font_size = font_size * scaling
            # font_sizeが小さい時はfont_sizeの調整が困難になる為、textureの拡大縮
            # 小のみに頼る
            if new_font_size < 10 and font_size < 10:
                pass
            else:
                self.font_size = new_font_size
                return
        pos = (pos[0] + self.x, pos[1] + self.y, )
        with canvas:
            rectangle = Rectangle(pos=pos, size=size, texture=self.texture)
        self._fl_rectangle = rectangle
        self.fl_scaling = scaling


def _calculate_pos_and_size_and_scaling(label_size, texture_size):
    '''(internal)

    Labelの大きさとTextureの大きさから、縦横比を維持してTextureをLabel内いっぱいに
    拡大/縮小したときのTextureの座標と拡大率を求める。'''
    l_width, l_height = label_size
    t_width, t_height = texture_size
    # check arguments
    if l_width <= 0 or l_height <= 0 or t_width <= 0 or t_height <= 0:
        return ((0, 0, ), (0, 0, ), 1, )
    # prefix 'r_' means 'rectangle_'
    t_aspect_ratio = t_width / t_height
    l_aspect_ratio = l_width / l_height
    if t_aspect_ratio < l_aspect_ratio:
        scaling = l_height / t_height
        r_width = scaling * t_width
        r_size = (r_width, l_height, )
        r_pos = ((l_width - r_width) / 2, 0, )
    else:
        scaling = l_width / t_width
        r_height = scaling * t_height
        r_size = (l_width, r_height, )
        r_pos = (0, (l_height - r_height) / 2, )
    return (r_pos, r_size, scaling, )


def _test():
    from kivy.base import runTouchApp
    from kivy.lang import Builder

    root = Builder.load_string(r'''
#:import FlexibleLabel __main__.FlexibleLabel
#:set FL_MAX_SCALING_MIN FlexibleLabel.FL_MAX_SCALING_MIN
#:set FL_MIN_SCALING_MIN FlexibleLabel.FL_MIN_SCALING_MIN
#:set FL_MIN_SCALING_MAX FlexibleLabel.FL_MIN_SCALING_MAX


BoxLayout:
    BoxLayout:
        orientation: 'vertical'
        AnchorLayout:
            size_hint_y: 0.8
            anchor_x: 'center'
            anchor_y: 'center'
            id: parent_of_flexible
            FlexibleLabel:
                id: flexible
                fl_min_scaling: slider_min_scaling.value
                fl_max_scaling: slider_max_scaling.value
                size_hint_x: slider_size_hint_x.value
                size_hint_y: slider_size_hint_y.value
                text: id_textinput.text
                canvas.after:
                    Line:
                        rectangle: self.x, self.y, self.width, self.height
                        dash_offset: 4
                        dash_length: 2
        BoxLayout:
            size_hint_y: 0.2
            BoxLayout:
                size_hint_x: 0.5
                orientation: 'vertical'
                Label:
                    text: 'font_size: {}'.format(int(flexible.font_size))
                Label:
                    text: 'texture_scaling: {:.3}'.format(float(flexible.fl_scaling))
            TextInput:
                id: id_textinput
                text: 'Ohayo\nAnnyeong\nZaoan\nBonjour\nMorning'
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.3
        Label:
            text: 'min_texture_scaling: {:.3}'.format(slider_min_scaling.value)
        Slider:
            id: slider_min_scaling
            min: FL_MIN_SCALING_MIN + 0.05
            max: FL_MIN_SCALING_MAX - 0.05
            step: 0.05
            value: 0.7
        Widget:
        Label:
            text: 'max_texture_scaling: {:.3}'.format(slider_max_scaling.value)
        Slider:
            id: slider_max_scaling
            min: FL_MAX_SCALING_MIN + 0.05
            max: 4
            step: 0.05
            value: 2.0
        Widget:
        Label:
            text: 'size_hint_x: {:.2}'.format(slider_size_hint_x.value)
        Slider:
            id: slider_size_hint_x
            min: 0.1
            max: 1
            step: 0.02
            value: 0.5
        Widget:
        Label:
            text: 'size_hint_y: {:.2}'.format(slider_size_hint_y.value)
        Slider:
            id: slider_size_hint_y
            min: 0.1
            max: 1
            step: 0.02
            value: 0.5
        Widget:
''')
    runTouchApp(root)


if __name__ == '__main__':
    _test()
