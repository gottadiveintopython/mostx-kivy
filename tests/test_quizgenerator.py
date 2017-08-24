# -*- coding: utf-8 -*-

import unittest

import beforetest
import quizgenerator as qgen


class QuizGeneratorTest(unittest.TestCase):

    CHOICES = r'ABCD'

    def test_basic_usage(self):
        for language in qgen.languages():
            with self.assertRaises(AssertionError):
                qgen.generate_quiz(
                    choices=[],  # len(choices) must be >= 2
                    num_adjectives=2,
                    language=language)
            with self.assertRaises(AssertionError):
                qgen.generate_quiz(
                    choices=self.CHOICES,
                    num_adjectives=0,  # num_adjectives must be > 0
                    language=language)
            with self.assertRaises(AssertionError):
                qgen.generate_quiz(
                    choices=self.CHOICES,
                    # num_adjectives must be <= qgen.get_max_adjectives()
                    num_adjectives=qgen.get_max_adjectives() + 1,
                    language=language)
            quiz = qgen.generate_quiz(
                choices=self.CHOICES,
                num_adjectives=2,
                language=language)
            print(quiz)


if __name__ == r'__main__':
    unittest.main()
