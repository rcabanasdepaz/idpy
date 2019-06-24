from functools import reduce
from idpy.potentials.discrete.potential import Potential
from idpy.models.idiagram import NODE_TYPES
import random

from idpy.inference.heuristics import get_heuristic



class VariableElimination:


    def __init__(self, idiag, removal_order="random_choice"):

        self.idiag = idiag
        if isinstance(removal_order, list):
            if not idiag.partial_order.is_consistent(list(reversed(removal_order))):
                raise ValueError("Wrong removal order")
            self._removal_order = removal_order
        elif isinstance(removal_order, str):
            self._heuristic = get_heuristic(removal_order)
        else:
            raise ValueError("wrong format for input parameter removal_order")

        self.preconditions()


    def __reset_results(self,):

            self.meu = None
            self.optimal_policy = {}
            self.expected_util = {}
            self._removed = []


    def removal_order(self):
        while set(self._removed) != set(self.idiag.variables):
            if self._removal_order:
                yield self._removal_order.pop(0)
            else:
                yield self._heuristic(self._probs, self._utils, self._removable_vars())


    def preconditions(self):
        self.idiag.add_nonforgetting()
        is_valid, msg = self.idiag.is_valid_id()

        if not is_valid:
            for m in msg: print(msg)


    def _removable_vars(self):      # move to partial order?

        if not self._removed:
            vars = self.idiag.partial_order._sets[-1]
        else:

            last_node = self._removed[-1]
            vars = self.idiag.partial_order.siblings(last_node) - set(self._removed)
            if not vars:
                vars = set(self.idiag.partial_order.graph.predecessors(last_node))

        return vars

    def run(self):

        self.__reset_results()

        # prepare current sets
        self._probs = set(self.idiag.prob_potentials.values())   #make pots hashables
        self._utils = set(self.idiag.util_potentials.values())

        for Y in self.removal_order():
            # select potentials with y
            probs_y = {p for p in self._probs if Y in p.domain.keys()}
            utils_y = {u for u in self._utils if Y in u.domain.keys()}

            # combine
            py = Potential.prod(probs_y)
            uy = Potential.sum(utils_y)
            # remove

            if idiag.is_node_type(Y, NODE_TYPES.CHANCE):
                pmarg = py.sum_marg(Y)
                umarg = (py * uy).sum_marg(Y)/ pmarg
            else:
                if py != None:
                    pmarg = py.restrict({Y:0})
                umarg = uy.max_marg(Y)

                # record the optimal policy and EU for decision
                self.optimal_policy.update({Y:uy.arg_max(Y)})
                self.expected_util.update({Y:uy})

            # update
            self._probs = self._probs - probs_y
            if py != None:
                self._probs = set.union(self._probs, {pmarg})
            self._utils = set.union(self._utils - utils_y, {umarg})


            self._removed.append(Y)


        self.meu = list(self._utils)[0].values



if __name__ == "__main__":

    from idpy.models.examples import wildcatter

    idiag = wildcatter()
    removal_order = ["O", "D", "S", "T"]

    inf = VariableElimination(idiag, removal_order)
    inf.run()

    print(inf.meu)
    print(inf.optimal_policy["D"].values)