from functools import reduce
from idpy.potentials.discrete.potential import Potential
from idpy.models.idiagram import NODE_TYPES


class VariableElimination:


    def __init__(self, idiag, removal_order):

        self.idiag = idiag
        if isinstance(removal_order, list):
            if not idiag.partial_order.is_consistent(list(reversed(removal_order))):
                raise ValueError("Wrong removal order")
            self.removal_order = (v for v in removal_order)


    def run(self):

        # prepare current sets
        probs = set(self.idiag.prob_potentials.values())   #make pots hashables
        utils = set(self.idiag.util_potentials.values())

        for Y in self.removal_order:

            # select potentials with y
            probs_y = {p for p in probs if Y in p.domain.keys()}
            utils_y = {u for u in utils if Y in u.domain.keys()}

            # combine

            py = Potential.prod(probs_y)
            uy = Potential.sum(utils_y)

            # remove

            if idiag.is_node_type(Y, NODE_TYPES.CHANCE):
                pmarg = py.sum_marg(Y)
                umarg = (py * uy).sum_marg(Y)/ pmarg
            else:
                pass # todo

            # update

            probs = probs - probs_y + {pmarg}
            utils = utils - utils_y + {umarg}





removal_order = ["O", "D", "S", "T"]
Y = "O"

from idpy.models.examples import wildcatter
from idpy.util.math import PartialOrder

idiag = wildcatter()
idiag.add_nonforgetting()
self = VariableElimination(idiag, removal_order)

self.run()

