from abc import ABC, abstractmethod
import numpy as np
from enum import IntEnum
from functools import reduce


class Potential(ABC):
    def __init__(self, values, variables, head):

        if len(variables) != len(set(variables)):
            raise ValueError("Variable list contains duplicate elements")

        if not self._check_cardinality(values, variables):
            raise ValueError("Cardinality Error")

        self._values = values
        self._variables = variables

        super().__init__()

    @property
    def variables(self):
        return self._variables

    @property
    def values(self):
        return self._values

    @property
    def kind(self):
        return self._kind

    @property
    def head(self):
        return self._head
    @property
    def tail(self):
        return self._tail

    @property
    @abstractmethod
    def cardinality(self):
        pass

    @abstractmethod
    def reorder(self, var_order):
        pass

    @staticmethod
    @abstractmethod
    def _check_cardinality(values, variables):
        pass

    @property
    def str_vars(self):
        return ",".join(self.variables)

    def get_var_card(self, v):
        return self.cardinality[self.get_var_index(v)]

    def get_var_index(self, v):
        if v not in self.variables:
            raise ValueError(f"Error: {v} not present in {self.short_repr()}")

        gen = (i for i, e in enumerate(self.variables) if e == v)
        return next(gen)

    @property
    def domain(self):
        return {v:c for v,c in zip(self.variables, self.cardinality)}

    @staticmethod
    @abstractmethod
    def _mult_values(op1, op2):
        pass


    def copy(self):
        new_vals = self.values.copy()
        new_kind = self.kind
        new_vars = self.variables.copy()

        new_head = []
        if new_kind is KIND.PROBABILITY:
            new_head = self.head.copy()

        return self.builder(new_kind, new_vals, new_vars, new_head)



    def _marg(self, var, operation):

        if var not in self.variables:
            raise ValueError(f"Error, variable '{var}' not present in the domain")

        new_vals = operation(self.get_var_index(var))
        new_kind = self.kind
        new_vars = [v for v in self.variables if v != var]

        new_head = []
        if new_kind is KIND.PROBABILITY:
            new_head = [v for v in new_vars if v in self.head]

        return self.builder(new_kind, new_vals, new_vars, new_head)

    def sum_marg(self, var):
        return self._marg(var, self._reduce_sum)
    def max_marg(self, var):
        return self._marg(var, self._reduce_max)



    def compare(self, other, operation):
        if other == None:
            return False
        #check that are comparable
        if self.domain != other.domain:
            return False

        self.reorder(other.variables)

        return operation(self, other)



    def combine(self, other, operation):
        op1 = self.copy()
        op2 = other.copy()

        if op1.__class__.__name__ != op2.__class__.__name__:
            raise ValueError("Multiplying 2 potentials of different structure type")

        new_domain = {**op1.domain, **op2.domain}

        if len(op1.variables) < len(new_domain):
            op1 = op1.extend_domain(new_domain)

        if len(op2.variables) < len(new_domain):
            op2 = op2.extend_domain(new_domain)

        op2.reorder(op1.variables)

        new_kind = min(op1.kind, op2.kind)
        new_vals = operation(op1,op2)
        new_vars = list(new_domain.keys())

        new_head = []
        if new_kind is KIND.PROBABILITY:
            new_head = [v for v in new_vars if v in op1.head or v in op2.head]


        return self.builder(new_kind, new_vals, new_vars, new_head)

    def __mul__(self, other):
        return self.combine(other, self._mult_values)

    def __rmul__(self, other):
        return other.combine(self, other._mult_values)

    def __add__(self, other):
        return self.combine(other, self._add_values)

    def __radd__(self, other):
        return other.combine(self, other._add_values)

    def __sub__(self, other):
        return self.combine(other, self._sub_values)

    def __rsub__(self, other):
        return other.combine(self, other._sub_values)

    def __truediv__(self, other):
        return self.combine(other, self._div_values)

    def __rtruediv__(self, other):
        return other.combine(self, other._div_values)


    def __eq__(self, other):
        return self.compare(other, self._eq_values)

    def __req__(self, other):
        return other.compare(self, other._eq_values)

    def __hash__(self):
        return hash(self.short_repr())

    def __repr__(self):

        card_str = ",".join([f"{v}:{self.get_var_card(v)}" for v in self.variables])

        return f"<Potential {self._kind.name[0:4].lower()}({self.str_vars}), cardinality = ({card_str})>"


    def short_repr(self):
        return f"{self._kind.name[0:1].lower()}({self.str_vars})"

    @staticmethod
    def prod(pot_list):
        res =  None
        if len(pot_list) > 1:
            res = reduce(lambda p1, p2: p1 * p2, pot_list)
        elif len(pot_list) == 1:
            res = list(pot_list)[0]
        return res

    @staticmethod
    def sum(pot_list):
        res =  None
        if len(pot_list) > 1:
            res = reduce(lambda p1, p2: p1 + p2, pot_list)
        elif len(pot_list) == 1:
            res = list(pot_list)[0]
        return res




class KIND(IntEnum):
    UTILITY = 0
    PROBABILITY = 1



class ProbabilityPotential(Potential):

    def __init__(self, *args,  **kwargs):
        variables = kwargs["variables"]
        head = kwargs["head"]

        if head is None: head = [variables[0]]

        self._kind = kwargs.pop("kind")


        self._head = [v for v in variables if v in head]
        self._tail = [v for v in variables if v not in head]


        super().__init__(*args, **kwargs)

    def is_valid_cpd(self):
        p = self
        for v in self.head:
            p = p.sum_marg(v)
        return np.all(p == p.get_unity(p.domain))


    @property
    def str_vars(self):

        str = ",".join(self.head)
        if len(self.tail)>0:
            str += "|" + ",".join(self.tail)
        return str

class UtilityPotential(Potential):
    def __init__(self, *args,  **kwargs):
        self._kind = kwargs.pop("kind")

        self._head = []
        self._tail = []

        super().__init__(*args, **kwargs)

