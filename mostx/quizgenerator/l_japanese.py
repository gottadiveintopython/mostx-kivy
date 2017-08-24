# -*- coding: utf-8 -*-
'''Mostx module for japanese'''

__all__ = [r'get_num_adjectives', r'generate_statement', r'generate_question']


ADJPAIRS_TEXT = \
    ''' 熱/冷た 厚/薄 大き/小さ 新し/古 鋭/鈍 美し/醜 近/遠 高/低
    細/太 堅/柔らか 易し/難し 明る/暗'''
ADJPAIRS = [i.split(sep=r'/', maxsplit=1) for i in ADJPAIRS_TEXT.split()]


def get_num_adjectives():
    return len(ADJPAIRS)


def generate_statement(a, b, adjpart):
    return r'{}は{}より{}い'.format(
        a, b, r'くて'.join(
            [ADJPAIRS[index][0 if is_forward_direction else 1] for (index, is_forward_direction) in adjpart]
        )
    )


def generate_question(index, is_forward_direction):
    return r'最も{}いのは?'.format(
        ADJPAIRS[index][0 if is_forward_direction else 1]
    )


if __name__ == r'__main__':
    print(get_num_adjectives())
    print(generate_statement(
        r'A', r'B',
        [(0, True,), (1, False,), (2, True,), ]
    ))
    print(generate_statement(
        r'C', r'D',
        [(3, False,), (4, True,), (5, False,), ]
    ))
    print(generate_question(6, True))
