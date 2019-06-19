import numpy as np
from idpy.potentials.discrete.potential import Potential, UtilityPotential, ProbabilityPotential, KIND


def build_potential_table(kind, *args, **kwargs):

    base = ProbabilityPotential if kind==KIND.PROBABILITY else UtilityPotential

    class PotentialTable(base):
        def __init__(self, kind, values, variables, head=None):

            ## some preprocess and checks ??
            # ....
            self.builder = build_potential_table
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
            idx_var_order = [self.get_var_index(v) for v in var_order]
            self.get_var_index("a")
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



    return PotentialTable(kind, *args, **kwargs)


p = build_potential_table(KIND.PROBABILITY, [[0.3,0.5, 0.4], [0.7,0.5, 0.6]], variables=["a", "b"], head=["a"])
u = build_potential_table(KIND.UTILITY, [20,30], variables=["a"])

p==p

# TODO:
# review head policy
# marginalize operations
# graph representation

pmarg = p.sum_marg("b") # check results


pa_b = build_potential_table(KIND.PROBABILITY, [[0.3,0.5, 0.4], [0.7,0.5, 0.6]], variables=["a", "b"], head=["a"])

pb = build_potential_table(KIND.PROBABILITY, [0.4, 0.2, 0.5], variables=["b"])

isinstance(pa_b, ProbabilityPotential)

pa_b.is_valid_cpd()
pb.is_valid_cpd()

pa_b.domain