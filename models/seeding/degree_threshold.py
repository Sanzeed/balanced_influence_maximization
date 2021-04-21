from .base import DiffusionModel


class ThresholdSeedingModel(DiffusionModel):
    def __init__(self, graph, majority, get_diffusion_probability, num_rels, threshold_dev, k):
        super(ThresholdSeedingModel, self).__init__(graph, 
                                                    majority, 
                                                    get_diffusion_probability, 
                                                    num_rels)
        self.threshold_dev = threshold_dev
        self.k = k
        self.active_set_map = {i : set() for i in range(self.num_rels)}
        self.majority_set_map = {i : set() for i in range(self.num_rels)}
        self.seeding_data = {'active_set' : None,
                             'majority' : None,
                             'seeds' : None}
        
    def __compute_majority_fraction(self):
        majority_count = 0
        
        for node in self.graph.nodes():
            if self.graph.node[node]['label'] == self.majority:
                majority_count += 1
                
        return majority_count / len(self.graph.nodes())
        
    def __choose_seeds(self):
        p_a = self.__compute_majority_fraction()
        k_maj = int(self.k * p_a) + self.threshold_dev
        k_min = self.k - k_maj
        
        if k_min < 0:
            return None
        
        majority_nodes, minority_nodes = [], []
        for node in self.graph.nodes():
            if self.graph.node[node]['label'] == self.majority:
                majority_nodes.append(node)
            else:
                minority_nodes.append(node)
        
        seeds = (sorted(majority_nodes, 
                key = lambda node : -self.graph.out_degree(node))[:k_maj]
                + sorted(minority_nodes, 
                key = lambda node : -self.graph.out_degree(node))[:k_min])
        
        return seeds
    
    def generate_seeding_data(self):
        self.seeding_data['seeds'] = self.__choose_seeds()
        if self.seeding_data['seeds'] == None:
            return self.seeding_data
        
        for seed in self.seeding_data['seeds']:
            for rel_index in range(self.num_rels):
                influence, majority = self.compute_influence_data(rel_index, seed)
                self.active_set_map[rel_index].update(influence)
                self.majority_set_map[rel_index].update(majority)
                
        self.seeding_data['active_set'] = sum(map(len, self.active_set_map.values())) / self.num_rels
        self.seeding_data['majority'] = sum(map(len, self.majority_set_map.values())) / self.num_rels
        
        return self.seeding_data
        