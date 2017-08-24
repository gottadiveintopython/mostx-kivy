# -*- coding: utf-8 -*-

import io
import os
import os.path
import json
import copy


class QuizSettings:

    def __init__(self, *, filepath):
        self._filepath = filepath
        if os.path.isfile(filepath):
            self.load()
        else:
            self.reset()

    def reset(self):
        self.data = copy.deepcopy(DEFAULT_SETTINGS)

    def load(self):
        with io.open(self._filepath, r'rt', encoding=r'utf-8') as reader:
            self.data = json.loads(reader.read(), parse_int=int, parse_constant=bool)

    def save(self):
        with io.open(self._filepath, r'wt', encoding=r'utf-8') as writer:
            writer.write(json.dumps(self.data, indent=4))


DEFAULT_SETTINGS = {
    r'endless': {
        r'release': {
            r'choices': r'ABCDEFG',
            r'time': 60,
            r'levels': [
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': True,
                    r'time_increament': 10,
                    r'num_clear_to_next_level': 5,
                },
                {
                    r'num_choices': 4,
                    r'time_increament': 15,
                    r'num_clear_to_next_level': 10,
                },
                {
                    r'num_adjectives': 2,
                    r'time_increament': 20,
                    r'num_clear_to_next_level': 15,
                },
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': False,
                    r'num_clear_to_next_level': 25,
                },
                {
                    r'num_adjectives': 2,
                    r'time_increament': 30,
                    r'num_clear_to_next_level': 35,
                },
                {
                    r'num_choices': 4,
                    r'time_increament': 60,
                    r'num_clear_to_next_level': -1,
                },
            ],
        },
        r'debug': {
            r'choices': r'ABCDEFG',
            r'time': 30,
            r'levels': [
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': True,
                    r'time_increament': 10,
                    r'num_clear_to_next_level': 1,
                },
                {
                    r'num_choices': 4,
                    r'time_increament': 15,
                    r'num_clear_to_next_level': 2,
                },
                {
                    r'num_adjectives': 2,
                    r'time_increament': 20,
                    r'num_clear_to_next_level': 3,
                },
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': False,
                    r'num_clear_to_next_level': 4,
                },
                {
                    r'num_adjectives': 2,
                    r'time_increament': 30,
                    r'num_clear_to_next_level': 5,
                },
                {
                    r'num_choices': 4,
                    r'time_increament': 60,
                    r'num_clear_to_next_level': -1,
                },
            ],
        },
    },
    r'timeattack': {
        r'release': {
            r'choices': r'ABCDEFG',
            r'levels': [
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': True,
                    r'num_clear_to_next_level': 5,
                },
                {
                    r'num_choices': 4,
                    r'num_clear_to_next_level': 10,
                },
                {
                    r'num_adjectives': 2,
                    r'num_clear_to_next_level': 15,
                },
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': False,
                    r'num_clear_to_next_level': 19,
                },
                {
                    r'num_adjectives': 2,
                    r'num_clear_to_next_level': 20,
                },
            ],
        },
        r'debug': {
            r'choices': r'ABCDEFG',
            r'levels': [
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': True,
                    r'num_clear_to_next_level': 1,
                },
                {
                    r'num_choices': 4,
                    r'num_clear_to_next_level': 2,
                },
                {
                    r'num_adjectives': 2,
                    r'num_clear_to_next_level': 3,
                },
                {
                    r'num_adjectives': 1,
                    r'num_choices': 3,
                    r'is_show_question_with_facts': False,
                    r'num_clear_to_next_level': 4,
                },
                {
                    r'num_adjectives': 3,
                    r'num_clear_to_next_level': 5,
                },
            ],
        },
    },
}
