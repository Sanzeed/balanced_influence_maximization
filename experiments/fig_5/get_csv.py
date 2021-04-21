import csv
import json

FIG_DATA_ROOT = './fig_data/'
N = 20000
P_M = 0.8
HS = [0.5, 0.8]
B_P = 0.01
H_PS = [0.5, 0.8]
DIV_WEIGHTS = [1.0, 0.8, 0.5, 0.2, 0.0]
GAMMAS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
NUM_GRAPHS = 10


def get_path(n, p_M, h, b_p, h_p, div_weight, gamma, graph_index):
    return ((FIG_DATA_ROOT 
             + '/n_' + str(n)
             + '/p_M_' + str(p_M)
             + '/h_' + str(h)
             + '/b_p_' + str(b_p)
             + '/h_p_' + str(h_p)
             + '/div_weight_' + str(div_weight)
             + '/gamma_' + str(gamma)
             + '/data_for_graph_' + str(graph_index) + '.json'))

def get_csv():
    fig5_csv = open('./fig5_csv.csv', 'w')
    writer = csv.writer(fig5_csv, delimiter = ',')
    writer.writerow(['h', 'h_p', 'lambda', 'gamma', 'run_index', 'active_set', 'majority'])
    for h in HS:
        for h_p in H_PS:
            for div_weight in DIV_WEIGHTS:
                for gamma in GAMMAS:
                    for graph_index in range(NUM_GRAPHS):
                        data = json.load(open(get_path(N, 
                                                       P_M, 
                                                       h, 
                                                       B_P, 
                                                       h_p, 
                                                       div_weight,
                                                       gamma, 
                                                       graph_index), 'r'))
                        writer.writerow([h, 
                                         h_p, 
                                         div_weight, 
                                         gamma, 
                                         graph_index, 
                                         data['active_set']['200'], 
                                         data['majority']['200']])
    fig5_csv.close()
    
if __name__ == '__main__':
    get_csv()