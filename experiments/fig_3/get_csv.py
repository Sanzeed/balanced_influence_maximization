import csv
import json

FIG_DATA_ROOT = './fig_data/'
B_PS = [0.01, 0.05, 0.1]
NS = [20000]
P_MS = [0.5, 0.6, 0.7, 0.8]
HS = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
NUM_GRAPHS = 20


def get_path(n, p_M, h, b_p, graph_index):
    return (FIG_DATA_ROOT 
            + '/n_' + str(n)
            + '/p_M_' + str(p_M)
            + '/h_' + str(h)
            + '/b_p_' + str(b_p)
            + '/data_for_graph_' + str(graph_index) + '.json')

def get_csv():
    fig3 = open('./fig3_csv.csv', 'w')
    writer = csv.writer(fig3, delimiter = ',')
    writer.writerow(['b_p', 'n', 'p_M', 'h', 'run_index', 'active_set', 'majority'])
    for b_p in B_PS:
        for n in NS:
            for p_M in P_MS:
                for h in HS:
                    for graph_index in range(NUM_GRAPHS):
                        data = json.load(open(get_path(n, p_M, h, b_p, graph_index), 'r'))
                        writer.writerow([b_p, 
                                         n, 
                                         p_M, 
                                         h, 
                                         graph_index, 
                                         data['active_set']['200'], 
                                         data['majority']['200']])
    fig3.close()
    
if __name__ == '__main__':
    get_csv()