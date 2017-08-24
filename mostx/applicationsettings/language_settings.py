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
        self.data = {r'english': {r'enable': True, r'font_name': DEFAULT_FONT}}
        self.detect_new_languages()

    def load(self):
        with io.open(self._filepath, r'rt', encoding=r'utf-8') as reader:
            self.data = json.loads(reader.read(), parse_int=int, parse_constant=bool)
        self.detect_new_languages()

    def save(self):
        with io.open(self._filepath, r'wt', encoding=r'utf-8') as writer:
            writer.write(json.dumps(self.data, indent=4))

    def detect_new_languages(self):
        detected_languages = list(self.data.keys())
        for language in quizgenerator.languages():
            if language not in detected_languages:
                print(r'Detected a new language :', language)
                self.data[language] = {r'enable': False, r'font_name': r''}

    def available_languages(self):
        r'''font_nameに値が設定されていてenableがTrueの言語を列挙'''
        def predicate(item):
            value = item[1]
            font_name = value[r'font_name']
            return value[r'enable'] is True and font_name and font_name != r''
        return filter(predicate, self.data.items())
