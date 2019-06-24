import networkx as nx
import numpy as np


class PartialOrder():
    def __init__(self, order_list):

        self.graph = nx.DiGraph()
        self._sets = [set(s) for s in order_list]

        for i in range(len(order_list) - 1):
            # for j in range(i+1, len(order_list)):
            j = i + 1
            for x in order_list[i]:
                for y in order_list[j]:
                    self.graph.add_edge(x, y)





    def siblings(self, node):
        return {y for x in [self.graph.successors(n)
                            for n in self.graph.predecessors(node)]
                for y in x} - {node}




    def with_commom_child(self, node):
        return {y for x in [self.graph.predecessors(n)
                            for n in self.graph.successors(node)]
                for y in x} - {node}



    def is_consistent(self, order):
        for i in range(len(order)-1):
            if self.graph.has_successor(order[i+1], order[i]):
                return False
        return True