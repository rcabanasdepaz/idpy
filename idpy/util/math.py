import networkx as nx
import numpy as np


class PartialOrder():
    def __init__(self, order_list):

        self.graph = nx.DiGraph()

        for i in range(len(order_list) - 1):
            # for j in range(i+1, len(order_list)):
            j = i + 1
            for x in order_list[i]:
                for y in order_list[j]:
                    print(f"({x}, {y})")
                    self.graph.add_edge(x, y)

    def is_consistent(self, order):
        for i in range(len(order)-1):
            if self.graph.has_successor(order[i+1], order[i]):
                return False
        return True


