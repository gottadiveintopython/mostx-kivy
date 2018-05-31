# -*- coding: utf-8 -*-

import unittest
from tempfile import TemporaryDirectory
from os.path import join as ospath_join
from kivy.core.text import DEFAULT_FONT

import beforetest
from langsettings import LangSettings


class Test(unittest.TestCase):

    def test_initial_value(self):
        with TemporaryDirectory() as tempdir:
            langsettings = LangSettings(ospath_join(tempdir, 'test_langsettings.json'))
            self.assertDictEqual(
                langsettings.data['english'],
                {'enable': True, 'font_name': DEFAULT_FONT}
            )
            for lang, value in langsettings.data.items():
                if lang == 'english':
                    continue
                self.assertDictEqual(value, {'enable': False, 'font_name': ''})

    def test_available_langs(self):
        with TemporaryDirectory() as tempdir:
            langsettings = LangSettings(ospath_join(tempdir, 'test.json'))
            data = langsettings.data
            data['english'].update(enable=False)
            data['japanese'].update(enable=True, font_name='yutapon')
            data['chinese'].update(enable=True, font_name='uming.ttc')
            self.assertDictEqual(
                {lang: value for lang, value in langsettings.available_langs()},
                {
                    'japanese': {'enable': True, 'font_name': 'yutapon'},
                    'chinese': {'enable': True, 'font_name': 'uming.ttc'},
                },
            )


if __name__ == '__main__':
    unittest.main()
