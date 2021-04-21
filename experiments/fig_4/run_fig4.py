import sys
sys.path.append('../')
sys.path.append('../../')
import click
import os
import json
from joblib import Parallel, delayed

from models.seeding.vanilla_greedy import VanillaSeedingModel
from helper_methods import *

RAW_DATA_ROOT = '../../raw_data/homophilic_directed_graphs/'
FIG_DATA_ROOT = './fig_data/'
P_MS = [0.5, 0.6, 0.7, 0.8]
H_S = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
H_PS = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
NUM_RELS = 10000
K = 200
NUM_GRAPHS = 20


def dump_seeding_data_file(n, p_M, h, b_p, h_p, k, graph_index):
    graph_path = (RAW_DATA_ROOT 
                  + '/n_' + str(n)
                  + '/p_M_' + str(p_M)
                  + '/h_' + str(h)
                  + '/graph_' + str(graph_index) + '.json')
    
    graph = fetch_graph(graph_path + '.json')
    majority = calculate_majority(graph)
    
    theta = calculate_theta(graph)
    get_diffusion_probability = (lambda u, v, u_label, v_label : 
        get_homophilic_diffusion_probability(graph, u, v, theta, b_p, h_p))
            
    seeder = VanillaSeedingModel(graph = graph,
                                 majority = majority, 
                                 get_diffusion_probability = get_diffusion_probability, 
                                 num_rels = NUM_RELS,
                                 k = K)
    fig_data = seeder.generate_seeding_data()
    
    dump_path = (FIG_DATA_ROOT 
                 + '/n_' + str(n)
                 + '/p_M_' + str(p_M)
                 + '/h_' + str(h)
                 + '/h_p_' + str(h_p)
                 + '/b_p_' + str(b_p)
                 + '/data_for_graph_' + str(graph_index) + '.json')
    os.makedirs(os.path.dirname(dump_path), exist_ok = True)
    json.dump(fig_data, open(dump_path, 'w'), indent = 2)
    
@click.command()
@click.option('--n', default = 20000)
@click.option('--b_p', default = 0.01)
@click.option('--n_jobs', default = 2)
def run_script(n, b_p, n_jobs):
    param_collection = [(graph_index, p_M, h)
                         for graph_index in range(NUM_GRAPHS)
                         for p_M in P_MS
                         for h in H_S
                         for h_p in H_PS]
    
    parallel = Parallel(n_jobs = n_jobs, verbose=10)
    parallel(
        delayed(dump_seeding_data_file)(
            n = n,
            p_M = p_M,
            h = h,
            b_p = b_p,
            h_p = h_p,
            k = K,
            graph_index = graph_index
        )
        for (graph_index, p_M, h, h_p) in param_collection
    )

if __name__ == "__main__":
    run_script() 

