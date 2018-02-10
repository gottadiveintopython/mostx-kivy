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
import applicationstate

kivy.require(r'1.9.1')


class MostxApp(App):

    def build(self):
        self.root = root = ScreenManager()
        self._appstate = appstate = applicationstate.create_default()
        appstate.funcs.update(
            switch_screen=_create_function_switch_screen(root),
            play_sound=_create_function_play_sound(),
        )
        appstate.data.update(
            records=applicationsettings.Records(
                filepath=os.path.join(self.user_data_dir, r'records.json')
            ),
            lang_settings=applicationsettings.LanguageSettings(
                filepath=os.path.join(self.user_data_dir, r'language_settings.json')
            ),
            quiz_settings=applicationsettings.QuizSettings(
                filepath=os.path.join(self.user_data_dir, r'quiz_settings.json')
            ),
            devmode=False,
        )
        root.add_widget(Screen(name=r'blank'))
        _setup_all_scenes(root, appstate)
        return root

    def on_start(self):
        self._appstate.funcs.switch_screen(r'title')

    def on_stop(self):
        self._appstate.data.records.save()
        self._appstate.data.lang_settings.save()
        self._appstate.data.quiz_settings.save()

    def on_pause(self):
        return True


def _create_function_switch_screen(screenmanager):

    def switch_screen(name, transition=NoTransition()):
        screenmanager.transition = transition
        screenmanager.current = name

    return switch_screen


def _create_function_play_sound():

    directory = os.path.join(os.path.curdir, r'data', r'sound')
    key_filename_dict = {
        r'intro': r'se_maoudamashii_effect05.ogg',
        r'bween': r'se_maoudamashii_retro03.ogg',
        r'ti': r'se_maoudamashii_system17.ogg',
        r'newrecord': r'se_maoudamashii_jingle07.ogg',
        r'rank-in': r'se_maoudamashii_jingle01.ogg',
        r'correct': r'se_maoudamashii_onepoint30.ogg',
        r'incorrect': r'se_maoudamashii_onepoint33.ogg',
        r'count': r'se_maoudamashii_system13.ogg',
    }
    sounds = {
        key: SoundLoader.load(os.path.join(directory, filename))
        for key, filename in key_filename_dict.items()
    }

    def play_sound(key):
        sound = sounds[key]
        if sound.state == r'play':
            sound.stop()
        sound.play()

    return play_sound


def _setup_all_scenes(screenmanager, appstate):
    scene_names = [
        r'title', r'menu', r'countdown', r'language_settings', r'records',
        r'quiz_endless', r'quiz_timeattack', r'result', r'credits',
    ]
    for name in scene_names:
        module = importlib.import_module(r'scenes.scene_' + name)
        screenmanager.add_widget(module.instantiate(appstate=appstate))


def _main():
    kivy.resources.resource_add_path(
        os.path.join(os.path.curdir, r'data', r'image'))
    kivy.resources.resource_add_path(
        os.path.join(os.path.curdir, r'data', r'text'))
    MostxApp().run()


if __name__ == r'__main__':
    _main()
