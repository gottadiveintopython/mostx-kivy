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
        with io.open(self._filepath, 'rt', encoding='utf-8') as reader:
            self.data = json.loads(reader.read(), parse_int=int, parse_constant=bool)

    def save(self):
        with io.open(self._filepath, 'wt', encoding='utf-8') as writer:
            writer.write(json.dumps(self.data, indent=4))


DEFAULT_SETTINGS = {
    'endless': {
        'release': {
            'choices': 'ABCDEFG',
            'time': 60,
            'levels': [
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': True,
                    'time_increament': 10,
                    'num_clear_to_next_level': 5,
                },
                {
                    'num_choices': 4,
                    'time_increament': 15,
                    'num_clear_to_next_level': 10,
                },
                {
                    'num_adjectives': 2,
                    'time_increament': 20,
                    'num_clear_to_next_level': 15,
                },
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': False,
                    'num_clear_to_next_level': 25,
                },
                {
                    'num_adjectives': 2,
                    'time_increament': 30,
                    'num_clear_to_next_level': 35,
                },
                {
                    'num_choices': 4,
                    'time_increament': 60,
                    'num_clear_to_next_level': -1,
                },
            ],
        },
        'debug': {
            'choices': 'ABCDEFG',
            'time': 30,
            'levels': [
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': True,
                    'time_increament': 10,
                    'num_clear_to_next_level': 1,
                },
                {
                    'num_choices': 4,
                    'time_increament': 15,
                    'num_clear_to_next_level': 2,
                },
                {
                    'num_adjectives': 2,
                    'time_increament': 20,
                    'num_clear_to_next_level': 3,
                },
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': False,
                    'num_clear_to_next_level': 4,
                },
                {
                    'num_adjectives': 2,
                    'time_increament': 30,
                    'num_clear_to_next_level': 5,
                },
                {
                    'num_choices': 4,
                    'time_increament': 60,
                    'num_clear_to_next_level': -1,
                },
            ],
        },
    },
    'timeattack': {
        'release': {
            'choices': 'ABCDEFG',
            'levels': [
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': True,
                    'num_clear_to_next_level': 5,
                },
                {
                    'num_choices': 4,
                    'num_clear_to_next_level': 10,
                },
                {
                    'num_adjectives': 2,
                    'num_clear_to_next_level': 15,
                },
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': False,
                    'num_clear_to_next_level': 19,
                },
                {
                    'num_adjectives': 2,
                    'num_clear_to_next_level': 20,
                },
            ],
        },
        'debug': {
            'choices': 'ABCDEFG',
            'levels': [
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': True,
                    'num_clear_to_next_level': 1,
                },
                {
                    'num_choices': 4,
                    'num_clear_to_next_level': 2,
                },
                {
                    'num_adjectives': 2,
                    'num_clear_to_next_level': 3,
                },
                {
                    'num_adjectives': 1,
                    'num_choices': 3,
                    'is_show_question_with_facts': False,
                    'num_clear_to_next_level': 4,
                },
                {
                    'num_adjectives': 3,
                    'num_clear_to_next_level': 5,
                },
            ],
        },
    },
}
