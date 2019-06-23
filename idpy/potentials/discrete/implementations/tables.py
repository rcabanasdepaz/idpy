import numpy as np
from idpy.potentials.discrete.potential import Potential, UtilityPotential, ProbabilityPotential, KIND


def potential_table(kind, *args, **kwargs):

    base = ProbabilityPotential if kind==KIND.PROBABILITY else UtilityPotential

    class PotentialTable(base):
        def __init__(self, kind, values, variables, head=None):

            ## some preprocess and checks ??
            # ....
            self.builder = potential_table
            super().__init__(kind=kind, values=np.array(values), variables=variables, head=head)

        @property
        def cardinality(self):
            return np.shape(self.values)

        @staticmethod
        def _check_cardinality(values, variables):
            return np.ndim(values) == len(variables)

        @staticmethod
        def get_unity(dict_vars):

            return PotentialTable(kind.PROBABILITY,
                                  np.ones(tuple(dict_vars.values())),
                                  variables = list(dict_vars.keys()),
                                  head=[])


        def reorder(self, var_order):
            if len(self.variables)<2:
                return
            idx_var_order = [var_order.index(v) for v in self._variables]
            self._values = np.moveaxis(self.values, range(np.ndim(self.values)), idx_var_order)
            self._variables = var_order

        def extend_domain(self, dict_vars):

            dict_vars = {v:c for v,c in dict_vars.items() if v not in self.variables}
            add_card = tuple(dict_vars.values())

            new_val = np.reshape(np.repeat(self.values, np.prod(add_card)), np.shape(self.values) + add_card)
            new_vars = self.variables + list(dict_vars.keys())

            return PotentialTable(self.kind, new_val, new_vars, self.head)


        @staticmethod
        def _mult_values(op1,op2):
            return op1.values * op2.values

        @staticmethod
        def _add_values(op1,op2):
            return op1.values + op2.values

        @staticmethod
        def _sub_values(op1,op2):
            return op1.values - op2.values

        @staticmethod
        def _div_values(op1,op2):
            return op1.values / op2.values

        @staticmethod
        def _eq_values(op1, op2):
            return op1.values == op2.values

        def _reduce_sum(self, axis):
            return np.sum(self.values, axis)
        def _reduce_max(self, axis):
            return np.max(self.values, axis)

        def _reduce_argmax(self, axis):
            return np.argmax(self.values, axis)

        def _restrict_values(self, conf):

            items = []
            for v in self._variables:
                if v in conf.keys():
                    items.append(conf[v])
                else:
                    items.append(slice(None))

            return self._values[tuple(items)]





    return PotentialTable(kind, *args, **kwargs)

