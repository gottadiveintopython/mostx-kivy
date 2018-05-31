# -*- coding: utf-8 -*-

from pathlib import Path
import importlib
import random
import itertools

from .attrdict import attrdict

__all__ = ('generate_quiz', 'langs', 'max_n_adjectives', )


LANG_DIR = Path(__file__).parent / 'langs'
LANGS = tuple(sorted(item.stem for item in LANG_DIR.iterdir() if not item.stem.startswith('__')))
LANG_MODULES = {
    lang: importlib.import_module('.langs.' + lang, __name__) for lang in LANGS
}
MAX_N_ADJECTIVES = min(
    lang_module.max_n_adjectives()
    for lang_module in LANG_MODULES.values())


def langs():
    '''`generate_quiz()`の引数`lang`に使える値を挙げるIterable'''
    return LANGS


def max_n_adjectives():
    '''`generate_quiz()`の引数`n_adjectives`に渡せる最大値'''
    return MAX_N_ADJECTIVES


def generate_quiz(*, choices, n_adjectives, lang, random_instance=random.Random()):
    '''Quizを作るMethod

    choices          ... 答えの選択肢を2つ以上挙げてくれるIterable
    n_adjectives   ... 問題文に使用する形容詞の数。この値は1からmax_n_adjectives()の範囲である必要がある
    language         ... 問題文の言語。`langs()`が返す値のいずれかを渡す必要がある
    戻り値 ... 作られたQuiz。型は属性のようにもアクセスできる辞書。
        .statements ... 問題の「AはBより...」といった文のlist。listの最後の要素には「最も〜は?」といった質問文が入っている。
        .choices ... 答えの選択肢のlist。
        .answer ... 正しい答え。choicesの要素のどれか。
    '''
    lang_module = LANG_MODULES.get(lang)
    if lang_module is None:
        raise ValueError("Unknown language '{}'.".format(lang))
    # check arguments
    choices = tuple(choices)
    assert 2 <= len(choices)
    assert n_adjectives == int(n_adjectives)
    n_adjectives = int(n_adjectives)
    assert 1 <= n_adjectives and n_adjectives <= MAX_N_ADJECTIVES

    # 問題文に使用する形容詞を無作為に選ぶ
    indices = random_instance.sample(range(lang_module.max_n_adjectives()), n_adjectives)
    # 選ばれた形容詞毎にchoices内の要素の順序を決定
    table = []
    for index in indices:
        order = list(choices)
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
    statements = []
    # 定義文(例: AはBより大きい)を生成
    for combination in combinations:
        a, b = combination[0], combination[1],
        adjpart_arg = [(index, order.index(a) < order.index(b),) for (index, order) in table]
        random_instance.shuffle(adjpart_arg)
        statements.append(lang_module.generate_statement(a, b, adjpart_arg))
    # Quizの答えを決定して、質問文(例: 最も大きのは？)を生成
    index, order = random_instance.choice(table)
    answer_index = random_instance.choice([0, -1])
    statements.append(lang_module.generate_question(index, answer_index == 0))
    return attrdict(
        statements=tuple(statements),
        answer=order[answer_index],
        choices=choices)
