from tsc_hellings import *

grammar = {
    'S': [['A', 'T']],
    'T': [['B', 'C']],
    'A': [['a']], 'B': [['b']], 'C': [['c']]
}
left_context = {'B': {'A'}, 'C': {'B'}}
right_context = {}

two_sided_context_hellings(grammar, left_context, right_context, "aabbcc")  # True
