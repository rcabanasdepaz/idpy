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

        self.preconditions()

        self.meu = None
        self.optimal_policy = {}
        self.expected_util = {}


    def preconditions(self):
        self.idiag.add_nonforgetting()
        is_valid, msg = self.idiag.is_valid_id()

        if not is_valid:
            for m in msg: print(msg)

    def run(self):

        # prepare current sets
        probs = set(self.idiag.prob_potentials.values())   #make pots hashables
        utils = set(self.idiag.util_potentials.values())

        for Y in self.removal_order:
            print(f"{probs} {utils}")
            print(f"remove {Y}")

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
                if py != None:
                    pmarg = py.restrict({Y:0})
                umarg = uy.max_marg(Y)

                # record the optimal policy and EU for decision
                self.optimal_policy.update({Y:uy.arg_max(Y)})
                self.expected_util.update({Y:uy})

            # update
            probs = probs - probs_y
            if py != None:
                probs = set.union(probs, {pmarg})
            utils = set.union(utils - utils_y, {umarg})

            # 2 potentials with the same domain

            print(f"{probs} {utils}")
        pass

        self.meu = list(utils)[0].values






from idpy.models.examples import wildcatter

idiag = wildcatter()
removal_order = ["O", "D", "S", "T"]

inf = VariableElimination(idiag, removal_order)

inf.run()

inf.meu
inf.expected_util["D"].values
inf.optimal_policy["D"].values

