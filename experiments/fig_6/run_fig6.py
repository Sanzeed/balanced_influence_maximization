import sys
sys.path.append('../')
sys.path.append('../../')
import click
import os
import json
from joblib import Parallel, delayed

from models.seeding.balanced_greedy import BalancedSeedingModel
from helper_methods import *

RAW_DATA_ROOT = '../../raw_data/twitter_graphs/'
FIG_DATA_ROOT = './fig_data/'
H_PS = [0.8, 0.5]
NUM_RELS = 1000
K = 200
NUM_RUNS = 5
DIV_WEIGHTS = [1.0, 0.8, 0.5, 0.2, 0.0]
GAMMAS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def dump_seeding_data_file(graph_name, b_p, h_p, k, div_weight, gamma, run_index):
    graph = fetch_graph(RAW_DATA_ROOT + graph_name + '.json')
    majority = calculate_majority(graph)
    
    theta = calculate_theta(graph)
    get_diffusion_probability = (lambda u, v, u_label, v_label : 
        get_homophilic_diffusion_probability(graph, u, v, theta, b_p, h_p))
        
    concave_transform = lambda x : x**0.5
    mu_func_weights = [concave_transform(gamma), 
                       concave_transform(1 - gamma)]
    
    seeder = BalancedSeedingModel(graph = graph,
                                  majority = majority, 
                                  get_diffusion_probability = get_diffusion_probability, 
                                  num_rels = NUM_RELS,
                                  k = K, 
                                  concave_transform = concave_transform, 
                                  div_weight = div_weight, 
                                  mu_func_weights = mu_func_weights)
    fig_data = seeder.generate_seeding_data()
    
    dump_path = (FIG_DATA_ROOT 
                 + graph_name
                 + '/b_p_' + str(b_p)
                 + '/h_p_' + str(h_p)
                 + '/div_weight_' + str(div_weight)
                 + '/gamma_' + str(gamma)
                 + '/run_' + str(run_index) + '.json')
    os.makedirs(os.path.dirname(dump_path), exist_ok = True)
    json.dump(fig_data, open(dump_path, 'w'), indent = 2)
    
@click.command()
@click.option('--graph_name', default = 'hersheycareers')
@click.option('--b_p', default = 0.01)
@click.option('--n_jobs', default = 2)
def run_script(graph_name, b_p, n_jobs):
    param_collection = [(run_index, h_p, div_weight, gamma)
                         for run_index in range(NUM_RUNS)
                         for h_p in H_PS
                         for div_weight in DIV_WEIGHTS
                         for gamma in GAMMAS]
    
    parallel = Parallel(n_jobs = n_jobs, verbose=10)
    parallel(
        delayed(dump_seeding_data_file)(
            graph_name = graph_name,
            b_p = b_p,
            h_p = h_p,
            k = K,
            div_weight = div_weight,
            gamma = gamma,
            run_index = run_index,
        )
        for (run_index, h_p, div_weight, gamma) in param_collection
    )

if __name__ == "__main__":
    run_script()