import numpy as np
import idpy.potentials.discrete.potential as idpot
import tensorflow as tf

# global tf_session
sess = tf.Session()



@idpot.prob_or_util
class PotentialTensor(idpot.ProbabilityPotential, idpot.UtilityPotential):
    def __init__(self, kind, values, variables, head=None):

        def builder(kind, *args, **kwargs):
            return PotentialTensor(kind, *args, **kwargs)

        self.builder = builder
        super(self.__class__, self).__init__(kind=kind, values=tf.convert_to_tensor(values), variables=variables, head=head)

    @property
    def cardinality(self):
        return self.values.get_shape().as_list()

    @staticmethod
    def _check_cardinality(values, variables):
        return sess.run(tf.rank(values)) == len(variables)
        # default session??
    @staticmethod
    def get_unity(dict_vars):

        return PotentialTensor(idpot.KIND.PROBABILITY,
                              tf.ones(tuple(dict_vars.values())),
                              variables = list(dict_vars.keys()),
                              head=[])


    def reorder(self, var_order):
        if len(self.variables)<2:
            return
        idx_var_order = [var_order.index(v) for v in self._variables]
        self._values = tf.transpose(self.values, perm=idx_var_order)
        self._variables = var_order

    def extend_domain(self, dict_vars):

        dict_vars = {v:c for v,c in dict_vars.items() if v not in self.variables}
        add_card = tuple(dict_vars.values())

        new_val = tf.reshape(tf.stack([self.values for _ in range(np.prod(add_card))],axis=-1),
                   tuple(self.values.get_shape().as_list()) + add_card)
        new_vars = self.variables + list(dict_vars.keys())

        return self.builder(self.kind, new_val, new_vars, self.head)

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
        return tf.reduce_sum(self.values, axis)
    def _reduce_max(self, axis):
        return tf.reduce_max(self.values, axis)

    def _reduce_argmax(self, axis):
        return tf.argmax(self.values, axis)

    def _restrict_values(self, conf):

        items = []
        for v in self._variables:
            if v in conf.keys():
                items.append(conf[v])
            else:
                items.append(slice(None))

        return self._values[tuple(items)]


    def _copy_values(self):
        return tf.identity(self._values)
