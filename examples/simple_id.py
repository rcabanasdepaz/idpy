from idpy.models.idiagram import *
from idpy.potentials.discrete.potential import Potential, UtilityPotential, ProbabilityPotential, KIND
from idpy.potentials.discrete.implementations.tables import *

self = IDiagram()
self.add_node("u", NODE_TYPES.UTILITY)
self.add_node("x", NODE_TYPES.CHANCE)
self.add_node("d2", NODE_TYPES.DECISION)
self.add_node("a", NODE_TYPES.CHANCE)
self.add_node("d1", NODE_TYPES.DECISION)


self.add_arc("x","u")
self.add_arc("d2", "x")
self.add_arc("d2", "u")
self.add_arc("a", "d2")
self.add_arc("d1", "a")


upot = PotentialTable(KIND.UTILITY, [[20, 30, 10], [0, 1, -4]], variables=["x", "d2"])
px_d1 = PotentialTable(KIND.PROBABILITY, [[0.3, 0.5, 0.4], [0.7, 0.5, 0.6]], variables=["x", "d2"])
pa_d2 = PotentialTable(KIND.PROBABILITY, [[0.4, 0.2], [0.3, 0.1], [0.3, 0.7]], variables=["a", "d1"])

self.add_prob_potentials(px_d1, pa_d2)
self.add_potential("u", upot)


self.get_direct_predecessors("x")

self.is_valid_id()

self.add_nonforgetting()


upot.short_repr()


