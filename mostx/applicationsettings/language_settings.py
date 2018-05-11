# -*- coding: utf-8 -*-

import io
import os
import os.path
import json

from kivy.core.text import DEFAULT_FONT

import quizgenerator


class LanguageSettings:

    def __init__(self, *, filepath):
        self._filepath = filepath
        if os.path.isfile(filepath):
            self.load()
        else:
            self.reset()

    def reset(self):
        self.data = {'english': {'enable': True, 'font_name': DEFAULT_FONT}}
        self.detect_new_languages()

    def load(self):
        with io.open(self._filepath, 'rt', encoding='utf-8') as reader:
            self.data = json.loads(reader.read(), parse_int=int, parse_constant=bool)
        self.detect_new_languages()

    def save(self):
        with io.open(self._filepath, 'wt', encoding='utf-8') as writer:
            writer.write(json.dumps(self.data, indent=4))

    def detect_new_languages(self):
        detected_languages = list(self.data.keys())
        for language in quizgenerator.languages():
            if language not in detected_languages:
                print('Detected a new language :', language)
                self.data[language] = {'enable': False, 'font_name': ''}

    def available_languages(self):
        '''font_nameに値が設定されていてenableがTrueの言語を列挙'''
        def predicate(item):
            value = item[1]
            font_name = value['font_name']
            return value['enable'] is True and font_name and font_name != ''
        return filter(predicate, self.data.items())
