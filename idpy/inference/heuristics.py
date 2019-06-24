import random
import operator
import sys

heuristics_all = ["random_choice", "min_size"]


def random_choice(probs, utils, variables, *args, **kwargs):
    print("random")
    return random.choice(list(vars))


def min_size(probs, utils, variables, *args, **kwargs):

    cost = {}

    for Y in variables:
        pots_y = {p for p in set.union(probs, utils) if Y in p.domain.keys()}

        clique = {}
        for p in pots_y:
            clique.update(p.domain)

        cost.update({Y : len(clique)})

    return __min(cost)


def __min(cost):
    return min(cost.items(), key=operator.itemgetter(1))[0]



def get_heuristic(name):
    if name not in heuristics_all:
        raise ValueError(f"Undefined heuristic {name}")
    return getattr(sys.modules[__name__], name)


