# -*- coding: utf-8 -*-

'''Quizを自動で作る機能を提供するModule

このModuleは以下の様なQuizを自動で作ってくれます(英語の場合)。

B is slower than A
A is faster than C
B is faster than C
Which is the slowest one?

# Usage(使い方)

import quizgenerator

list(quizgenerator.languages()) # => [r'chinese', r'english', r'korean', r'japanese']

quiz = quizgenerator.generate_quiz(
    choices=r'ABC',
    num_adjectives=1,
    language=r'english')
print(quiz)
# Quiz
#   facts : ['B is slower than A', 'A is faster than C', 'B is faster than C']
#   question : Which is the slowest one?
#   choices : ['A', 'B', 'C']
#   answer : C

quiz = quizgenerator.generate_quiz(
    choices=[r'Onion', r'Cabbage', r'Cucumber'],
    num_adjectives=2,
    language=r'english')
print(quiz)
# Quiz
#   facts :
#       ['Onion is newer,quieter than Cucumber',
#        'Cabbage is quieter,newer than Cucumber',
#        'Cabbage is noisier,older than Onion']
#   question : Which is the noisiest one?
#   choices : ['Onion', 'Cabbage', 'Cucumber']
#   answer : Cucumber
'''

import importlib
import random
import itertools

from smartobject import SmartObject

__all__ = [r'generate_quiz', r'languages', r'get_max_adjectives']


LANGS = r'japanese korean chinese english'.split()
langm_dict = {lang: importlib.import_module(r'.l_' + lang, r'quizgenerator') for lang in LANGS}
MAX_ADJECTIVES = min([langm.get_num_adjectives() for langm in langm_dict.values()])


def languages():
    r'"generate_quiz"の"language"引数に使える値を挙げるIterable'
    return LANGS


def get_max_adjectives():
    r'"generate_quiz"の"num_adjectives"引数の最大値'
    return MAX_ADJECTIVES


def generate_quiz(*, choices, num_adjectives, language, random_instance=random.Random()):
    r'''Quizを作るMethod

    choices          ... 答えの選択肢を2つ以上挙げてくれるIterable
    num_adjectives   ... 問題文に使用する形容詞の数。この値は1からget_max_adjectives()の範囲である必要がある
    language         ... 問題文の言語。languages()が返す値のいずれかを渡す必要がある
    戻り値 ... 作られたQuiz。以下の属性を持っている。
        .facts ... 問題の[AはBより...]といった文のlist。
        .question ... 問題の質問文(最も...のは？)。
        .choices ... 答えの選択肢が入ったlist
        .answer ... 正しい答え。choicesの要素のどれか。
    '''
    langm = langm_dict[language]
    # check arguments
    choices = list(choices)
    assert 2 <= len(choices)  # 2以上
    assert 1 <= num_adjectives and num_adjectives <= MAX_ADJECTIVES  # 1以上MAX_ADJECTIVES以下

    # 問題文に使用する形容詞をRandomに選択
    indices = random_instance.sample(range(langm.get_num_adjectives()), num_adjectives)
    # 形容詞毎にchoices内の要素の順序を決定
    table = []
    for index in indices:
        order = choices[:]
        random_instance.shuffle(order)
        table.append((index, order,))
    # choicesの要素を2つ取り出す場合に有り得る組み合わせを求める
    combinations = []
    for combination in itertools.combinations(choices, 2):
        combination = list(combination)  # tupleはShuffle出来ないのでlistに変換
        random_instance.shuffle(combination)
        combinations.append(combination)
    random_instance.shuffle(combinations)
    # --------------------------------------------------------------------
    # 文を生成
    # --------------------------------------------------------------------
    facts = []
    # 条件文のlistを生成
    for combination in combinations:
        a, b = combination[0], combination[1],
        adjpart_arg = [(index, order.index(a) < order.index(b),) for (index, order) in table]
        random_instance.shuffle(adjpart_arg)
        facts.append(langm.generate_statement(a, b, adjpart_arg))
    # Quizの答えを決定して、質問文(例: 最も大きのは？)を生成
    index, order = random_instance.choice(table)
    answer_index = random_instance.choice([0, -1])
    return SmartObject(
        so_name=r'Quiz',
        facts=facts,
        answer=order[answer_index],
        question=langm.generate_question(index, answer_index == 0),
        choices=choices).so_as_readonly()
