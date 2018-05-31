# -*- coding: utf-8 -*-

__all__ = ('QuizSettings', )

from pathlib import Path
import json
from kivy.resources import resource_find


class QuizSettings:

    def __init__(self, filepath):
        self.filepath = filepath = Path(filepath)
        if filepath.exists():
            self.load()
        else:
            self.reset()

    def reset(self):
        filepath = Path(resource_find('default_quiz_settings.json'))
        self.data = json.loads(
            filepath.read_text(encoding='utf-8'),
            parse_int=int,
            parse_constant=bool,
        )

    def load(self):
        self.data = json.loads(
            self.filepath.read_text(encoding='utf-8'),
            parse_int=int,
            parse_constant=bool,
        )

    def save(self):
        self.filepath.write_text(
            json.dumps(self.data, indent=4),
            encoding='utf-8',
        )
