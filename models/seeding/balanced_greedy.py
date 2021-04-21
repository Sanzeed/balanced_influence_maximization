import numpy as np

from .base import GreedySeedingModel


class BalancedSeedingModel(GreedySeedingModel):
    def __init__(self, graph, majority, get_diffusion_probability, num_rels, k, concave_transform, div_weight, mu_func_weights):
        super(BalancedSeedingModel, self).__init__(graph, majority, get_diffusion_probability, num_rels, k)
        self.concave_transform = concave_transform
        self.div_weight = div_weight
        self.mu_func_weights = mu_func_weights
        
    def compute_expected_marginal_gain(self, v):
        new_influence_sum = 0
        new_diversity_sum = 0
        
        for rel_index in range(self.num_rels):
            v_influence, v_majority = self.compute_influence_data(rel_index, v)
            
            new_influence = len(v_influence.union(self.active_set_map[rel_index]))
            new_influence_sum += new_influence
            
            new_majority = len(v_majority.union(self.majority_set_map[rel_index]))
            new_minority = new_influence - new_majority
            new_diversity_sum += (self.mu_func_weights[0] * self.concave_transform(new_majority)
                                 + self.mu_func_weights[1] * self.concave_transform(new_minority))
        
        expected_influence = new_influence_sum / self.num_rels
        expected_diversity = new_diversity_sum / self.num_rels
                         
        influence_gain_normalizer = (1 - self.div_weight) / len(self.graph)
        diversity_gain_normalizer = self.div_weight / (self.mu_func_weights[0] * self.concave_transform(np.sum(self.group_vector)) 
                                                  + self.mu_func_weights[1] * self.concave_transform(np.sum(1 - self.group_vector)))
        new_objective = influence_gain_normalizer * expected_influence + diversity_gain_normalizer * expected_diversity
        
        return (new_objective - self.current_objective_value)
