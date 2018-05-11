# -*- coding: utf-8 -*-
'''Mostx module for korean'''

__all__ = ('get_num_adjectives', 'generate_statement', 'generate_question', )


ADJPAIRS_TEXT = \
    '''작/크 적/많 짧/길 가볍/무겁 좁/넓 가늘/굵 가깝/멀 춥/덥
    쉽/어렵 조용하/시끄럽 예쁘/더럽 맛있/맛없'''
ADJPAIRS = [i.split(sep='/', maxsplit=1) for i in ADJPAIRS_TEXT.split()]


def get_num_adjectives():
    return len(ADJPAIRS)


def generate_statement(a, b, adjpart):
    return '{}는 {}보다 {}다'.format(
        a, b, '고 '.join(
            [ADJPAIRS[index][0 if is_forward_direction else 1] for (index, is_forward_direction) in adjpart]
        )
    )


def generate_question(index, is_forward_direction):
    return '어느 것이 가장 {}다?'.format(
        ADJPAIRS[index][0 if is_forward_direction else 1]
    )


if __name__ == '__main__':
    print(get_num_adjectives())
    print(generate_statement(
        'A', 'B',
        [(0, True,), ]
    ))
    print(generate_statement(
        'A', 'B',
        [(0, True,), (1, False,), ]
    ))
    print(generate_statement(
        'C', 'D',
        [(3, False,), (4, True,), (5, False,), ]
    ))
    print(generate_question(6, True))
