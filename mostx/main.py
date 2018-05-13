# -*- coding: utf-8 -*-

import importlib
import os.path

import kivy
import kivy.resources
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.screenmanager import (
    Screen, ScreenManager, NoTransition
)

import applicationsettings
import applicationglobals

kivy.require('1.9.1')


class MostxApp(App):

    def build(self):
        self.root = root = ScreenManager()
        self._appglobals = appglobals = applicationglobals.create_default()
        appglobals.funcs.update(
            switch_screen=_create_function_switch_screen(root),
            play_sound=_create_function_play_sound(),
        )
        appglobals.data.update(
            records=applicationsettings.Records(
                filepath=os.path.join(self.user_data_dir, 'records.json')
            ),
            lang_settings=applicationsettings.LanguageSettings(
                filepath=os.path.join(self.user_data_dir, 'language_settings.json')
            ),
            quiz_settings=applicationsettings.QuizSettings(
                filepath=os.path.join(self.user_data_dir, 'quiz_settings.json')
            ),
            devmode=False,
        )
        root.add_widget(Screen(name='blank'))
        _setup_all_scenes(root, appglobals)
        return root

    def on_start(self):
        self._appglobals.funcs.switch_screen('title')

    def on_stop(self):
        self._appglobals.data.records.save()
        self._appglobals.data.lang_settings.save()
        self._appglobals.data.quiz_settings.save()

    def on_pause(self):
        return True


def _create_function_switch_screen(screenmanager):

    def switch_screen(name, transition=NoTransition()):
        screenmanager.transition = transition
        screenmanager.current = name

    return switch_screen


def _create_function_play_sound():

    directory = os.path.join(os.path.curdir, 'data', 'sound')
    key_filename_dict = {
        'intro': 'se_maoudamashii_effect05.ogg',
        'bween': 'se_maoudamashii_retro03.ogg',
        'ti': 'se_maoudamashii_system17.ogg',
        'newrecord': 'se_maoudamashii_jingle07.ogg',
        'rank-in': 'se_maoudamashii_jingle01.ogg',
        'correct': 'se_maoudamashii_onepoint30.ogg',
        'incorrect': 'se_maoudamashii_onepoint33.ogg',
        'count': 'se_maoudamashii_system13.ogg',
    }
    sounds = {
        key: SoundLoader.load(os.path.join(directory, filename))
        for key, filename in key_filename_dict.items()
    }

    def play_sound(key):
        sound = sounds[key]
        if sound.state == 'play':
            sound.stop()
        sound.play()

    return play_sound


def _setup_all_scenes(screenmanager, appglobals):
    scene_names = [
        'title', 'menu', 'countdown', 'language_settings', 'records',
        'quiz_endless', 'quiz_timeattack', 'result', 'credits',
    ]
    for name in scene_names:
        module = importlib.import_module('scenes.scene_' + name)
        screenmanager.add_widget(module.instantiate(appglobals=appglobals))


def _main():
    kivy.resources.resource_add_path(
        os.path.join(os.path.curdir, 'data', 'image'))
    kivy.resources.resource_add_path(
        os.path.join(os.path.curdir, 'data', 'text'))
    MostxApp().run()


if __name__ == '__main__':
    _main()
