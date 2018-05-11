# -*- coding: utf-8 -*-

import kivy
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.atlas import Atlas
from random import random

kivy.require('1.9.1')

__all__ = ('BouncingSprites',)


class Sprite(Scatter):
    velocity_x = NumericProperty(0)
    velocity_x_base = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity_y_base = NumericProperty(0)
    velocity_rotation = NumericProperty(0)

    def __init__(self, *, texture, **kwargs):
        super().__init__(
            do_scale=False,
            do_translation=False,
            do_rotation=True,
            size_hint=(None, None,),
            size=texture.size,
            **kwargs)
        image = Image(size_hint=(1, 1,), texture=texture)
        self.add_widget(image)


class BouncingSprites(FloatLayout):

    def __init__(self, *, atlasfilepath, **kwargs):
        super(BouncingSprites, self).__init__(**kwargs)
        self.clock_event = None
        atlas = Atlas(atlasfilepath)
        x, y, = self.pos
        width, height, = self.size
        for texture in atlas.textures.values():
            sprite = Sprite(texture=texture)
            sprite.x = x + random() * width
            sprite.y = y + random() * height
            sprite.velocity_x_base = sprite.velocity_x = random() * 5
            sprite.velocity_y_base = sprite.velocity_y = random() * 5
            sprite.velocity_rotation = random() * 5
            self.add_widget(sprite)

    def start_animation(self):
        if self.clock_event is None:
            self.clock_event = Clock.schedule_interval(self.animate, 0.05)

    def stop_animation(self):
        if self.clock_event is not None:
            self.clock_event.cancel()
            self.clock_event = None

    def animate(self, dt):
        width = self.width
        height = self.height
        for child in self.children:
            child.rotation += child.velocity_rotation
            child.x += child.velocity_x
            child.y += child.velocity_y
            if child.right > width:
                child.velocity_x = -child.velocity_x_base
            elif child.x < 0:
                child.velocity_x = child.velocity_x_base
            if child.top > height:
                child.velocity_y = -child.velocity_y_base
            elif child.y < 0:
                child.velocity_y = child.velocity_y_base
