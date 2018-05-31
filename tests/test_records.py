# -*- coding: utf-8 -*-

import unittest
from tempfile import TemporaryDirectory
from os.path import join as ospath_join

import beforetest
from records import Records


class Test(unittest.TestCase):

    def test_initial_value(self):
        with TemporaryDirectory() as tempdir:
            records = Records(ospath_join(tempdir, 'test_records.json'))
            self.assertDictEqual(
                records.data,
                {'endless': [], 'timeattack': [], }
            )


if __name__ == '__main__':
    unittest.main()
