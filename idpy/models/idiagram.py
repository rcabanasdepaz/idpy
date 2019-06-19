from enum import IntEnum

import networkx as nx


from idpy.potentials.discrete.potential import Potential, UtilityPotential, ProbabilityPotential, KIND


class IDiagram():
    def __init__(self):
        self._graph = nx.DiGraph()

    @property
    def graph(self):
        return self._graph

    @property
    def nodes(self):
        return list(self._graph.node.keys())

    def nodes_of_type(self, type):
        return [n for n,a in self._graph.node.items() if a["type"]==type]

    @property
    def decisions(self):
        return [n for n in nx.topological_sort(self._graph) if self.is_node_type(n, NODE_TYPES.DECISION)]
    @property
    def chancenodes(self):
        return self.nodes_of_type(NODE_TYPES.CHANCE)
    @property
    def utilitynodes(self):
        return self.nodes_of_type(NODE_TYPES.UTILITY)



    def is_node_type(self, node, nodetype):
        return self.get_node_info(node)["type"] == nodetype


    def get_direct_successors(self, node):
        return self._graph.successors(node)

    def get_direct_predecessors(self, node):
        return self._graph.predecessors(node)


    def get_node_info(self, id):
        return self._graph.node[id]

    @property
    def arcs(self):
        arc_list = []
        for x in self.nodes:
            for y in self.get_direct_successors(x):
                arc_list.append((x,y))
        return arc_list


    def add_arc(self, parent, child, check_flag=True):
        if check_flag:
            self.__check_arc_additon(parent,child)
        self._graph.add_edge(parent, child)

    def add_arcs(self, *arc_list):
        for a in arc_list:
            self.add_arc(a[0], a[1])



    def __check_arc_additon(self, parent, child):
        if parent not in self.nodes or child not in self.nodes:
            raise AssertionError(f"Any of the nodes in ({parent}->{child}) do not exist")

        if self.is_node_type(parent, NODE_TYPES.UTILITY):
            raise AssertionError(f"A utility node cannot contain outgoing arcs")



    def add_node(self, id, type):

        if not isinstance(type, NODE_TYPES):
            raise ValueError(f"Wrong node type {id}")

        self._graph.add_node(id, {"type": type, "potential":None})


    def add_potential(self, node, pot, check_flag=True):
        if check_flag:
            err_msg = self.__check_node_pot(node, pot)
            if err_msg != None:
                raise ValueError(err_msg)

        info = self.get_node_info(node)
        info.update({"potential": pot})
        self._graph.node.update({node: info})

    def add_prob_potentials(self, *potlist):
        for p in potlist: self.add_potential(p.head[0], p)


    def __check_node_pot(self, node, pot):

        msg = None
        if self.is_node_type(node, NODE_TYPES.DECISION):
            msg = "Potentials cannot be associated to decisions"

        if pot.kind == KIND.PROBABILITY:
            if not self.is_node_type(node, NODE_TYPES.CHANCE):
                msg = "A probability potential can only be added to chance nodes"

            if pot.head != [node]:
                msg = "Uncompatible head variables"

            if set(self.get_direct_predecessors(node)) !=  set(pot.tail):
                msg = "Chance node predecessors not compatible with this potential"


        if pot.kind == KIND.UTILITY:
            if not self.is_node_type(node, NODE_TYPES.UTILITY):
                msg = "A utility potential can only be added to utility nodes"



            if set(self.get_direct_predecessors(node)) !=  set(pot.variables):
                msg = "Utility predecessors not compatible with this potential"


        if msg != None: msg = msg + f". Node {node}, {pot}"
        return msg


    def get_potentials_from_nodes(self, nodes, exclude_none=True):
        pot_dict = {n: self._graph.node[n]["potential"] for n in nodes}
        if exclude_none:
            return {n:p for n,p in pot_dict.items() if p is not None}
        return pot_dict

    @property
    def potentials(self):
        return self.get_potentials_from_nodes(self.utilitynodes+self.chancenodes)

    @property
    def prob_potentials(self):
        return self.get_potentials_from_nodes(self.chancenodes)
    @property
    def util_potentials(self):
        return self.get_potentials_from_nodes(self.utilitynodes)


    def is_valid_id(self):

        msgs = []

        card_dict = {}
        # correct association of the potentials
        for node, pot in self.potentials.items():
            err_msg = self.__check_node_pot(node, pot)
            if err_msg != None:
                msgs.append(err_msg)

            # check cardinality
            for v,c in pot.domain.items():
                if v not in card_dict:
                    card_dict.update({v:c})
                else:
                    if c != card_dict[v]:
                        msgs.append(f"Incoherent cardinality of variable {v}")

        # check that there is not any node without potential
        pots = {n: self._graph.node[n]["potential"] for n in self.utilitynodes + self.chancenodes}
        if None in list(pots.values()):
            msgs.append("There are some chance or utility nodes without a poential")


        # no cycles
        if list(nx.simple_cycles(self._graph)) != []:
            msgs.append("There are some chance or utility nodes without a potential")


        return len(msgs)<1, msgs


    def add_nonforgetting(self):
        d = self.decisions

        if len(d)>1:
            for i in range(0,len(d)-1):
                pred_to_add = self.get_direct_predecessors(d[i]) + [d[i]]
                for j in range(i+1,len(d)):
                    for p in pred_to_add:
                        self.add_arc(p, d[j], check_flag=False)




class NODE_TYPES(IntEnum):
    CHANCE = 0
    DECISION = 1
    UTILITY = 2
