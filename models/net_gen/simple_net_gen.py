import numpy as np
import networkx as nx

from base import NetGen


class SimpleNetGen(NetGen):
    def __init__(self, n, p_M, alpha, beta, gamma, delta_in, delta_out):
        super(NetGen, self).__init__(n, p_M, alpha, beta, gamma, delta_in, delta_out)
        
    def __generate_in_probabilities(self, graph):
        in_degrees = np.array([graph.in_degree(node) 
                               for node in range(len(graph))])
        
        return (in_degrees + self.delta_in) / np.sum(in_degrees + self.delta_in)
    
    def __generate_out_probabilities(self, graph):
        out_degrees = np.array([graph.out_degree(node) 
                                for node in range(len(graph))])
        
        return (out_degrees + self.delta_out) / np.sum(out_degrees + self.delta_out)
    
    def __choose_node_by_in_degree(self, graph):
        nodes = np.array([node for node in range(len(graph))])
        probabilities = self.generate_in_probabilities(graph)
        return np.random.choice(nodes, 1, False, probabilities)[0]
    
    def __choose_node_by_out_degree(self, graph):
        nodes = np.array([node for node in range(len(graph))])
        probabilities = self.generate_out_probabilities(graph)
        return np.random.choice(nodes, 1, False, probabilities)[0]
    
    def add_new_node_with_out_edge(self, graph):
        v = len(graph)
        label = np.random.choice(['a', 'b'], 1, False, [self.p_M, 1 - self.p_M])[0]
        
        if len(graph) == 1:
            graph.add_edges_from([(v, 0)])
            return
            
        w = self.choose_node_by_in_degree(graph)
        graph.add_edges_from([(v, w)])
        
        nx.set_node_attributes(graph, {v : {'label' : label}})
    
    def add_new_edge_between_old_nodes(self, graph):
        if len(graph) == 1:
            return
            
        v = self.choose_node_by_out_degree(graph)
        w = self.choose_node_by_in_degree(graph)
        graph.add_edges_from([(v, w)])
    
    def add_new_node_with_in_edge(self, graph):
        w = len(graph)
        label = np.random.choice(['a', 'b'], 1, False, [self.p_M, 1 - self.p_M])[0]
        
        if len(graph) == 1:
            graph.add_edges_from([(0, w)])
            return
            
        v = self.choose_node_by_out_degree(graph)
        graph.add_edges_from([(v, w)])
        
        nx.set_node_attributes(graph, {w : {'label' : label}})