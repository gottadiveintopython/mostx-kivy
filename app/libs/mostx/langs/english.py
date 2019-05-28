# -*- coding: utf-8 -*-
'''Mostx module for english'''

__all__ = ('max_n_adjectives', 'generate_statement', 'generate_question', )


ADJSTEXT = \
    ''' smaller,smallest/larger,largest
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
    '''internal use'''
    result = []
    for line in adjtext.split():
        pair = line.split(sep='/', maxsplit=1)
        result.append((
            pair[0].split(sep=',', maxsplit=1),
            pair[1].split(sep=',', maxsplit=1),
        ))
    return result


ADJS = construct_adjectives(ADJSTEXT)


def max_n_adjectives():
    return len(ADJS)


def generate_statement(a, b, adjpart):
    if len(adjpart) == 1:
        (index, is_forward_direction,) = adjpart[0]
        result = '{a} is {adjs} than {b}'.format(a=a, b=b, adjs=ADJS[index][0 if is_forward_direction else 1][0])
    else:
        adjs = [ADJS[index][0 if is_forward_direction else 1][0] for (index, is_forward_direction) in adjpart]
        lastadj = adjs.pop()
        result = '{a} is {adjs} and {lastadj} than {b}'.format(a=a, b=b, adjs=','.join(adjs), lastadj=lastadj)
    return result


def generate_question(index, is_forward_direction):
    return 'Which is the {}?'.format(
        ADJS[index][0 if is_forward_direction else 1][1]
    )


if __name__ == '__main__':
    print(max_n_adjectives())
    print(generate_statement(
        'A', 'B', [(0, True,), ]
    ))
    print(generate_statement(
        'A', 'B', [(0, True,), (1, False,), ]
    ))
    print(generate_statement(
        'C', 'D', [(3, False,), (4, True,), (5, False,), ]
    ))

    print(generate_question(6, True))
