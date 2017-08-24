# -*- coding: utf-8 -*-
'''Mostx module for english'''

__all__ = [r'get_num_adjectives', r'generate_statement', r'generate_question']


ADJSTEXT = \
    r''' smaller,smallest/larger,largest
         longer,longest/shorter,shortest
         colder,coldest/hotter,hottest
         newer,newest/older,oldest
         faster,fastest/slower,slowest
         nearer,nearest/farther,farthest
         harder,hardest/softer,softest
         fatter,fattest/thinner,thinnest
         sadder,saddest/happier,happiest
         quieter,quietest/noisier,noisiest'''


def construct_adjectives(adjtext):
    r'internal use'
    result = []
    for line in adjtext.split():
        pair = line.split(sep=r'/', maxsplit=1)
        result.append((
            pair[0].split(sep=r',', maxsplit=1),
            pair[1].split(sep=r',', maxsplit=1),
        ))
    return result


ADJS = construct_adjectives(ADJSTEXT)


def get_num_adjectives():
    return len(ADJS)


def generate_statement(a, b, adjpart):
    if len(adjpart) == 1:
        (index, is_forward_direction,) = adjpart[0]
        result = r'{a} is {adjs} than {b}'.format(a=a, b=b, adjs=ADJS[index][0 if is_forward_direction else 1][0])
    else:
        adjs = [ADJS[index][0 if is_forward_direction else 1][0] for (index, is_forward_direction) in adjpart]
        lastadj = adjs.pop()
        result = r'{a} is {adjs} and {lastadj} than {b}'.format(a=a, b=b, adjs=r','.join(adjs), lastadj=lastadj)
    return result


def generate_question(index, is_forward_direction):
    return r'Which is the {}?'.format(
        ADJS[index][0 if is_forward_direction else 1][1]
    )


if __name__ == r'__main__':
    print(get_num_adjectives())
    print(generate_statement(
        r'A', r'B', [(0, True,), ]
    ))
    print(generate_statement(
        r'A', r'B', [(0, True,), (1, False,), ]
    ))
    print(generate_statement(
        r'C', r'D', [(3, False,), (4, True,), (5, False,), ]
    ))

    print(generate_question(6, True))
