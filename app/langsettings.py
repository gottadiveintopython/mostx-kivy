# -*- coding: utf-8 -*-

'''問題文に使用する言語と各言語を表示するのに使うFontの情報を保持する


# File名を与えて初期化する。Fileが存在していた場合は、その内容を読み込む。
langsettings = LangSettings('./filename.json')


# 各種設定をいじくる
data = langsettings.data
data['japanese'].enable = True  # 問題文に使う言語の一つに日本語を含める
data['japanese'].font_name = 'uming.ttc'  # 日本語の問題文の表示に利用するFontを'uming.ttc'に設定
data['english'].enable = True  # 問題文に使う言語の一つに英語を含める
data['english'].font_name = 'Roboto'  # 英語の問題文の表示に利用するFontを'Roboto'に設定


# 設定を保存
langsettings.save()  # 初期化時に与えたFileに書き込む
'''

__all__ = ('LangSettings', )

from pathlib import Path
import json
from kivy.core.text import DEFAULT_FONT

import mostx


class LangSettings:

    def __init__(self, filepath):
        self.filepath = filepath = Path(filepath)
        if filepath.exists():
            self.load()
        else:
            self.reset()

    def reset(self):
        self.data = {'english': {'enable': True, 'font_name': DEFAULT_FONT}}
        self.detect_new_langs()

    def load(self):
        self.data = json.loads(
            self.filepath.read_text(encoding='utf-8'),
            parse_int=int,
            parse_constant=bool,
        )
        self.detect_new_langs()

    def save(self):
        self.filepath.write_text(
            json.dumps(self.data, indent=4),
            encoding='utf-8',
        )

    def detect_new_langs(self):
        detected_langs = list(self.data.keys())
        for lang in mostx.langs():
            if lang not in detected_langs:
                # print('Detected a new language:', lang)
                self.data[lang] = {'enable': False, 'font_name': ''}

    def available_langs(self):
        '''font_nameに値が設定されていてenableがTrueの言語を列挙'''
        def predicate(item):
            value = item[1]
            font_name = value['font_name']
            return value['enable'] is True and font_name
        return filter(predicate, self.data.items())
