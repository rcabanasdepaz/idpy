from idpy.potentials.discrete.implementations.tables import *
from idpy.potentials.discrete.implementations.tensors import *
import idpy.potentials.discrete.potential as idpot

import tensorflow as tf

def table_to_tensor(ptable):
    args = [ptable.kind, ptable.values, ptable.variables]

    if ptable.kind == idpot.KIND.PROBABILITY:
        args.append(ptable.head)

    return PotentialTensor(*args)


def tensor_to_table(ptensor):
    args = [ptensor.kind, ptensor.values, ptensor.variables]

    if ptensor.kind == idpot.KIND.PROBABILITY:
        args.append(ptensor.head)

    args = [sess.run(a) if isinstance(a, tf.Tensor) else a for a in args]

    return PotentialTable(*args)

