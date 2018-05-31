# -*- coding: utf-8 -*-

'''Quizの成績を保持する


# File名を与えて初期化する。Fileが存在していた場合は、その内容を読み込む。
records = Records('./filename.json')


# Quizの成績を追加(EndlessModeの場合)
records.add(
    mode='endless',
    result={
        'n_cleared': 2,
        'n_answered': 10,
        'langs': ('korean', 'english', ),
    }
)
# Quizの成績を追加(TimeAttackModeの場合)
records.add(
    mode='timeattack',
    result={
        'n_cleared': 2,
        'n_answered': 10,
        'langs': ('chinese', 'japanese', ),
        'points': 1234,
        'time': 4321,
    }
)


# 保存
records.save()  # 初期化時に与えたFileに書き込む
'''

from pathlib import Path
import json
import datetime


class Records:

    MAX_RECORDS = 100

    def __init__(self, filepath):
        self.filepath = filepath = Path(filepath)
        if filepath.exists():
            self.load()
        else:
            self.reset()

    def reset(self):
        self.data = {'endless': [], 'timeattack': [], }

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

    def add(self, *, mode, result):
        '''新しい記録を登録する。戻り値は記録の順位(0から始まる)。ランク外だった場合はNone。'''
        data = result.copy()
        data['date'] = datetime.date.today().isoformat()
        sort_key = {'endless': 'n_cleared', 'timeattack': 'points'}[mode]
        rlist = self.data[mode]
        rlist.append(data)
        rlist.sort(key=(lambda x: x[sort_key]), reverse=True)  # sort_keyの大きい順に並べ替える
        if len(rlist) > self.MAX_RECORDS:
            rlist.pop()
        return_value = None
        for index, value in enumerate(rlist):
            if id(data) == id(value):
                return_value = index
                break
        return return_value
