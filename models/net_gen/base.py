import networkx as nx
import numpy as np


class NetGen:
    def __init__(self, n, p_M, alpha, beta, gamma, delta_in, delta_out):
        self.n = n
        self.p_M = p_M
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta_in = delta_in
        self.delta_out = delta_out

    def generate_initial_graph(self):
        graph = nx.DiGraph()
        graph.add_node(0)
        return graph
        
    def add_new_node_with_out_edge(self, graph):
        pass
    
    def add_new_edge_between_old_nodes(self, graph):
        pass
    
    def add_new_node_with_in_edge(self, graph):
        pass
    
    def generate_full_graph(self):
        graph = self.generate_initial_graph()
        possible_actions = [self.add_new_node_with_out_edge,
                            self.add_new_edge_between_old_nodes,
                            self.add_new_node_with_in_edge]
        terminate = False
        
        while not terminate:
            action = np.random.choice(possible_actions, 
                                      1, 
                                      True, 
                                      [self.alpha, self.beta, self.gamma])[0]
            action(graph)            
            terminate = len(graph) >= self.n
            
        return graph
        
        