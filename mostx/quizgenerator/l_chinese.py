# -*- coding: utf-8 -*-
'''Mostx module for chinese'''

__all__ = [r'get_num_adjectives', r'generate_statement', r'generate_question']


ADJPAIRS_TEXT = \
    ''' 快/慢 高/矮 早/晚 寬/窄 厚/薄 細/粗 容易/難 好/壞 長/短 大/小 熱/冷 新/舊 近/遠 貴/便宜'''
ADJPAIRS = [i.split(sep=r'/', maxsplit=1) for i in ADJPAIRS_TEXT.split()]


def get_num_adjectives():
    return len(ADJPAIRS)


def generate_statement(a, b, adjpart):
    if len(adjpart) == 1:
        (index, is_forward_direction,) = adjpart[0]
        result = r'{}比{}{}'.format(a, b, ADJPAIRS[index][0 if is_forward_direction else 1])
    else:
        result = r'{}比{}又{}'.format(
            a, b, r'又'.join(
                [ADJPAIRS[index][0 if is_forward_direction else 1] for (index, is_forward_direction) in adjpart]
            )
        )
    return result


def generate_question(index, is_forward_direction):
    return r'哪個最{}?'.format(
        ADJPAIRS[index][0 if is_forward_direction else 1]
    )


if __name__ == r'__main__':
    print(get_num_adjectives())
    print(generate_statement(
        r'A', r'B',
        [(0, True,), ]
    ))
    print(generate_statement(
        r'A', r'B',
        [(0, True,), (1, False,), ]
    ))
    print(generate_statement(
        r'C', r'D',
        [(3, False,), (4, True,), (6, True,), ]
    ))
    print(generate_question(6, True))
