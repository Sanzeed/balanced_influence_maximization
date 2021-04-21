import numpy as np
from scipy.stats import bernoulli
import heapq

class DiffusionModel:
    def __init__(self, graph, majority, get_diffusion_probability, num_rels):
        self.graph = graph
        self.majority = majority
        
        nodes = sorted(self.graph.nodes())
        self.node_index_map = {nodes[i] : i for i in range(len(nodes))}
        self.group_vector = np.array([int(graph.nodes[node]['label'] == majority) for node in nodes])
        
        self.num_rels = num_rels
        self.get_diffusion_probability = get_diffusion_probability
        self.__generate_live_edges()
    
    def __generate_live_edges(self):
        edges = list(self.graph.edges())
        self.live_edges = {}
        
        edge_probabilities = [self.get_diffusion_probability(u, v, 
                                                             self.graph.nodes[u]['label'],
                                                             self.graph.nodes[v]['label']) for (u, v) in edges]
        for i in range(self.num_rels):
            edge_life_indicators = bernoulli.rvs(edge_probabilities)
            self.live_edges[i] = {edges[i] for i in range(len(edges)) if edge_life_indicators[i]}
        
        assert len(self.live_edges) == self.num_rels
        
    def __is_live_edge(self, rel_index, u, v):        
        if self.graph.is_directed():
            return (u, v) in self.live_edges[rel_index]
        else:
            return (u, v) in self.live_edges[rel_index] or (v, u) in self.live_edges[rel_index]
    
    def compute_influence_data(self, rel_index, u):
        bfs_queue = {u}
        visited_nodes = set()
        influence_set, majority_in_influence_set = set(), set()
        
        while bfs_queue:
            node_to_visit = bfs_queue.pop()
            visited_nodes.add(node_to_visit)
            influence_set.add(node_to_visit)
            
            if self.graph.nodes[node_to_visit]['label'] == self.majority:
                majority_in_influence_set.add(node_to_visit)
                
            for neighbor in self.graph.neighbors(node_to_visit):
                if neighbor not in visited_nodes and self.__is_live_edge(rel_index, node_to_visit, neighbor):
                    bfs_queue.add(neighbor)
                    
        return influence_set, majority_in_influence_set
    
    def generate_seeding_data(self):
        pass

class GreedySeedingModel(DiffusionModel):
    def __init__(self, graph, majority, get_diffusion_probability, num_rels, k):
        super(GreedySeedingModel, self).__init__(graph, majority, get_diffusion_probability, num_rels)
        self.queue = [(float('-inf'), -1, v) for v in self.graph.nodes()]
        heapq.heapify(self.queue)
        self.k = k
        self.current_objective_value = 0
        self.active_set_map = {i : set() for i in range(self.num_rels)}
        self.majority_set_map = {i : set() for i in range(self.num_rels)}
        self.seeding_data = {'active_set' : {i + 1 : set() for i in range(self.k)},
                             'majority' : {i + 1 : set() for i in range(self.k)},
                             'seeds' : []}
        
    def compute_expected_marginal_gain(self, v):
        pass
        
    def do_next_iteration(self):
        inc, iter_flag, u = heapq.heappop(self.queue)
        
        if iter_flag == len(self.seeding_data['seeds']):
            self.seeding_data['seeds'].append(u)
            self.current_objective_value += -inc
            
            for rel_index in range(self.num_rels):
                influence, majority = self.compute_influence_data(rel_index, u)
                    
                self.active_set_map[rel_index].update(influence)
                self.majority_set_map[rel_index].update(majority)
                
            self.seeding_data['active_set'][iter_flag + 1] = sum(map(len, self.active_set_map.values())) / self.num_rels
            self.seeding_data['majority'][iter_flag + 1] = sum(map(len, self.majority_set_map.values())) / self.num_rels
            
        else:
            new_negated_marginal_gain = -self.compute_expected_marginal_gain(u)
            new_iter_flag = len(self.seeding_data['seeds'])
            heapq.heappush(self.queue, (new_negated_marginal_gain, new_iter_flag, u))
        
    def generate_seeding_data(self):        
        while len(self.seeding_data['seeds']) < self.k:
            self.do_next_iteration()
            
        return self.seeding_data
