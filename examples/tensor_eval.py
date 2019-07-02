from idpy.models.examples import wildcatter
from idpy.potentials.discrete.convert import convert_id, table_to_tensor
from idpy.inference.variable_elimination import *

from idpy.potentials.discrete.implementations.tensors import sess

# load a sample ID
idiag = wildcatter()

# convert potentials to tensor format
convert_id(idiag, table_to_tensor)

# run the inference
inf = VariableElimination(idiag, removal_order)
inf.run()

# print the results
sess.run(inf.meu)

# TODO: avoid multiple tf run??