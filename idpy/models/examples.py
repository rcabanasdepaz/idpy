from idpy.models.idiagram import *
from idpy.potentials.discrete.potential import Potential, UtilityPotential, ProbabilityPotential, KIND
from idpy.potentials.discrete.implementations.tables import *



def wildcatter():
    id = IDiagram()

    c, p ,t, d, s, o = ("C", "P", "T", "D", "S", "O")

    id.add_node(c, NODE_TYPES.UTILITY)
    id.add_node(p, NODE_TYPES.UTILITY)

    id.add_node(t, NODE_TYPES.DECISION)
    id.add_node(d, NODE_TYPES.DECISION)

    id.add_node(s, NODE_TYPES.CHANCE)
    id.add_node(o, NODE_TYPES.CHANCE)

    id.add_arcs((t,d), (t,s), (t,c), (o,s), (o,p), (s,d), (d,p))

    v=np.array([
    [[0.1, 0.3, 0.5], [1/3, 1/3, 1/3]],
    [[0.3, 0.4, 0.4], [1/3, 1/3, 1/3]],
    [[0.6, 0.3, 0.1], [1/3, 1/3, 1/3]]
    ])

    pS_TO = PotentialTable(KIND.PROBABILITY, v, variables=[s, t, o])
    pO = PotentialTable(KIND.PROBABILITY, [0.5, 0.3, 0.2], variables=[o])

    uDO = PotentialTable(KIND.UTILITY, [[-70, 50, 200], [0, 0, 0]], variables = [d, o])

    uT = PotentialTable(KIND.UTILITY, [-10, 0], t)

    id.add_prob_potentials(pS_TO, pO)
    id.add_potential(c, uT)
    id.add_potential(p, uDO)

    return id

