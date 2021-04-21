from .base import GreedySeedingModel


class VanillaSeedingModel(GreedySeedingModel):
    def __init__(self, graph, majority, get_diffusion_probability, num_rels, k):
        super(VanillaSeedingModel, self).__init__(graph, majority, get_diffusion_probability, num_rels, k)
    
    def compute_expected_marginal_gain(self, v):
        new_influence_sum = 0
        
        for rel_index in range(self.num_rels):
            v_influence, _ = self.compute_influence_data(rel_index, v)
            new_influence = len(v_influence.union(self.active_set_map[rel_index]))
            new_influence_sum += new_influence
        
        expected_influence = new_influence_sum / self.num_rels
                       
        influence_gain_normalizer = (1 - self.div_weight) / len(self.graph)
        new_objective = influence_gain_normalizer * expected_influence
        
        return (new_objective - self.current_objective_value)
