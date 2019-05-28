# -*- coding: utf-8 -*-

import importlib
import sys
from pathlib import Path
from kivy.resources import resource_add_path
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.screenmanager import Screen

APP_DIR = Path(__file__).parent
sys.path.append(str(APP_DIR / 'libs'))

from langsettings import LangSettings
from quizsettings import QuizSettings
from records import Records
from appglobals import AppGlobals
from customscreenmanager import MostxScreenManager


class MostxApp(App):

    appglobals = ObjectProperty(AppGlobals())

    def build_config(self, config):
        config.setdefaults('game', {'devmode': False, })

    def build_settings(self, settings):
        JSON_DATA = """[
            { "type": "title",
              "title": "Game Config" },

            { "type": "bool",
              "title": "Dev Mode",
              "section": "game",
              "key": "devmode" }
        ]"""
        settings.add_json_panel('Mostx', self.config, data=JSON_DATA)

    def on_config_change(self, config, section, key, value):
        if config is not self.config:
            return
        if (section, key, ) == ('game', 'devmode', ):
            self.appglobals.data.devmode = config.get('game', 'devmode') != '0'

    def build(self):
        self.root = root = MostxScreenManager()
        appglobals = self.appglobals
        appglobals.funcs.update(
            switch_scene=root.try_to_switch_screen,
            play_sound=_create_function_play_sound(),
        )
        user_data_dir = Path(self.user_data_dir)
        appglobals.update(
            records=Records(user_data_dir / 'records.json'),
            langsettings=LangSettings(user_data_dir / 'langsettings.json'),
            quizsettings=QuizSettings(user_data_dir / 'quizsettings.json'),
        )
        appglobals.data.devmode = self.config.get('game', 'devmode') != '0'
        root.add_widget(Screen(name='blank'))
        self._setup_all_scenes()
        return root

    def _setup_all_scenes(self):
        scene_dir = APP_DIR / 'scenes'
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

    sound_dir = APP_DIR.joinpath('data', 'sound', )
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
    resource_add_path(str(APP_DIR / 'data'))
    MostxApp().run()


if __name__ == '__main__':
    _main()
