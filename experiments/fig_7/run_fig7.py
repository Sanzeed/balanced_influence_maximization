import sys
sys.path.append('../')
sys.path.append('../../')
import click
import os
import json
from joblib import Parallel, delayed

from models.seeding.degree_threshold import ThresholdSeedingModel
from helper_methods import *

RAW_DATA_ROOT = '../../raw_data/twitter_graphs/'
FIG_DATA_ROOT = './fig_data/'
H_PS = [0.8, 0.5]
NUM_RELS = 1000
K = 200
NUM_RUNS = 5
THRESHOLD_DEV = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]


def dump_seeding_data_file(graph_name, b_p, h_p, k, run_index):
    graph = fetch_graph(RAW_DATA_ROOT + graph_name + '.json')
    majority = calculate_majority(graph)
    
    theta = calculate_theta(graph)
    get_diffusion_probability = (lambda u, v, u_label, v_label : 
        get_homophilic_diffusion_probability(graph, u, v, theta, b_p, h_p))
    
    fig_data = {str(threshold_dev) : None for threshold_dev in THRESHOLD_DEV}
    for threshold_dev in THRESHOLD_DEV:
        seeder = ThresholdSeedingModel(graph = graph,
                                   majority = majority, 
                                   get_diffusion_probability = get_diffusion_probability, 
                                   num_rels = NUM_RELS,
                                   threshold_dev = threshold_dev,
                                   k = K)
        print(threshold_dev)
        fig_data[str(threshold_dev)] = seeder.generate_seeding_data()
    
    dump_path = (FIG_DATA_ROOT 
                 + graph_name
                 + '/b_p_' + str(b_p)
                 + '/h_p_' + str(h_p)
                 + '/run_' + str(run_index) + '.json')
    os.makedirs(os.path.dirname(dump_path), exist_ok = True)
    json.dump(fig_data, open(dump_path, 'w'), indent = 2)

@click.command()
@click.option('--graph_name', default = 'hersheycareers')
@click.option('--b_p', default = 0.01)
@click.option('--n_jobs', default = 2)
def run_script(graph_name, b_p, n_jobs):
    param_collection = [(run_index, h_p)
                         for run_index in range(NUM_RUNS)
                         for h_p in H_PS]
    
    parallel = Parallel(n_jobs = n_jobs)
    parallel(
        delayed(dump_seeding_data_file)(
            graph_name = graph_name,
            b_p = b_p,
            h_p = h_p,
            k = K,
            run_index = run_index,
        )
        for (run_index, h_p) in param_collection
    )

if __name__ == "__main__":
    run_script()