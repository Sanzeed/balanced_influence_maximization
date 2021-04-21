import csv
import json

FIG_DATA_ROOT = './fig_data/'
B_PS = [0.01, 0.05, 0.1]
NS = [15000, 20000]
P_MS = [0.5, 0.6, 0.7, 0.8]
NUM_GRAPHS = 20


def get_path(n, p_M, b_p, graph_index):
    return (FIG_DATA_ROOT 
            + '/n_' + str(n)
            + '/p_M_' + str(p_M)
            + '/b_p_' + str(b_p)
            + '/data_for_graph_' + str(graph_index) + '.json')

def get_csv():
    fig1 = open('./fig1_csv.csv', 'w')
    writer = csv.writer(fig1, delimiter = ',')
    writer.writerow(['b_p', 'n', 'p_M', 'run_index', 'active_set', 'majority'])
    
    for b_p in B_PS:
        for n in NS:
            for p_M in P_MS:
                for graph_index in range(NUM_GRAPHS):
                    data = json.load(open(get_path(n, p_M, b_p, graph_index), 'r'))
                    writer.writerow([b_p, 
                                     n, 
                                     p_M, 
                                     graph_index, 
                                     data['active_set']['200'], 
                                     data['majority']['200']])
    fig1.close()
    
if __name__ == '__main__':
    get_csv()