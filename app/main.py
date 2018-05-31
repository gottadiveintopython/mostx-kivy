# -*- coding: utf-8 -*-

import importlib
import sys
from pathlib import PurePath, Path
from kivy.resources import resource_add_path
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.screenmanager import Screen

ROOT_DIRECTORY = PurePath(__file__).parents[1]
sys.path.insert(1, str(ROOT_DIRECTORY / 'lib'))

from langsettings import LangSettings
from quizsettings import QuizSettings
from records import Records
from appglobals import AppGlobals
from customscreenmanager import MostxScreenManager


class MostxApp(App):

    def build(self):
        self.root = root = MostxScreenManager()
        self.appglobals = appglobals = AppGlobals()
        appglobals.funcs.update(
            switch_scene=root.switch_screen,
            play_sound=_create_function_play_sound(),
        )
        user_data_dir = PurePath(self.user_data_dir)
        appglobals.update(
            records=Records(user_data_dir / 'records.json'),
            langsettings=LangSettings(user_data_dir / 'langsettings.json'),
            quizsettings=QuizSettings(user_data_dir / 'quizsettings.json'),
        )
        appglobals.data.devmode = False
        root.add_widget(Screen(name='blank'))
        self._setup_all_scenes()
        return root

    def _setup_all_scenes(self):
        scene_dir = Path(__file__).parent / 'scenes'
        scene_names = tuple(
            item.stem for item in scene_dir.iterdir()
            if (not item.stem.startswith('__')) and (
                item.is_dir() or (item.suffix == '.py')
            )
        )
        print(scene_names)
        add_widget = self.root.add_widget
        appglobals = self.appglobals
        for name in scene_names:
            module = importlib.import_module('scenes.' + name)
            add_widget(module.instantiate(name=name, appglobals=appglobals))

    def on_start(self):
        self.appglobals.funcs.switch_scene('title')

    def on_stop(self):
        appglobals = self.appglobals
        appglobals.records.save()
        appglobals.langsettings.save()
        # appglobals.quizsettings.save()


def _create_function_play_sound():

    sound_dir = PurePath(__file__).parent.joinpath('data', 'sound', )
    filename_dict = {
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
        key: SoundLoader.load(str(sound_dir / filename))
        for key, filename in filename_dict.items()
    }

    def play_sound(key):
        sound = sounds[key]
        if sound.state == 'play':
            sound.stop()
        sound.play()

    return play_sound


def _main():
    resource_add_path(str(PurePath(__file__).parent / 'data'))
    MostxApp().run()


if __name__ == '__main__':
    _main()
