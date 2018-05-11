# -*- coding: utf-8 -*-
'''Mostx module for japanese'''

__all__ = ('get_num_adjectives', 'generate_statement', 'generate_question', )


ADJPAIRS_TEXT = \
    ''' 熱/冷た 厚/薄 大き/小さ 新し/古 鋭/鈍 美し/醜 近/遠 高/低
    細/太 堅/柔らか 易し/難し 明る/暗'''
ADJPAIRS = [i.split(sep='/', maxsplit=1) for i in ADJPAIRS_TEXT.split()]


def get_num_adjectives():
    return len(ADJPAIRS)


def generate_statement(a, b, adjpart):
    return '{}は{}より{}い'.format(
        a, b, 'くて'.join(
            [ADJPAIRS[index][0 if is_forward_direction else 1] for (index, is_forward_direction) in adjpart]
        )
    )


def generate_question(index, is_forward_direction):
    return '最も{}いのは?'.format(
        ADJPAIRS[index][0 if is_forward_direction else 1]
    )


if __name__ == '__main__':
    print(get_num_adjectives())
    print(generate_statement(
        'A', 'B',
        [(0, True,), (1, False,), (2, True,), ]
    ))
    print(generate_statement(
        'C', 'D',
        [(3, False,), (4, True,), (5, False,), ]
    ))
    print(generate_question(6, True))
