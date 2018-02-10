# -*- coding: utf-8 -*-

import io
import os
import os.path
import json
import datetime


class Records:

    MAX_RECORDS = 10

    def __init__(self, *, filepath):
        self._filepath = filepath
        if os.path.isfile(filepath):
            self.load()
        else:
            self.clear()

    def clear(self):
        self.data = {r'endless': [], r'timeattack': [], }

    def load(self):
        with io.open(self._filepath, r'rt', encoding=r'utf-8') as reader:
            self.data = json.loads(reader.read(), parse_int=int, parse_float=float)

    def save(self):
        with io.open(self._filepath, r'wt', encoding=r'utf-8') as writer:
            writer.write(json.dumps(self.data, indent=4))

    def add(self, *, mode, result):
        r'新しい記録を登録する。戻り値は記録の順位(0から始まる)。ランク外だった場合は-1。'
        data = result.copy()
        data[r'date'] = datetime.date.today().isoformat()
        sort_key = {r'endless': r'num_cleared', r'timeattack': r'points'}[mode]
        rlist = self.data[mode]
        rlist.append(data)
        rlist.sort(key=(lambda x: x[sort_key]), reverse=True)  # sort_keyの大きい順に並べ替える
        if len(rlist) > self.MAX_RECORDS:
            rlist.pop()
        return_value = -1
        for index, value in enumerate(rlist):
            if id(data) == id(value):
                return_value = index
                break
        return return_value


def _test():
    import random
    obj = Records(filepath=r'./test_record.json')
    today = datetime.date.today().isoformat()
    for i in range(3):
        num_cleared = random.randrange(0, 20)
        obj.add(
            mode=r'endless',
            result={
                r'date': today,
                r'num_cleared': num_cleared,
                r'num_answered': 5
            }
        )
    for i in range(3):
        time = random.randrange(0, 40)
        obj.add(
            mode=r'timeattack',
            result={
                r'date': today,
                r'points': round(time * 20 / 25, 2),
                r'num_cleared': 20,
                r'num_answered': 25,
                r'time': time
            }
        )
    obj.save()


if __name__ == r'__main__':
    _test()
