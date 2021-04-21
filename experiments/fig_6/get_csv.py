import csv
import json

FIG_DATA_ROOT = './fig_data/'
NETWORKS = ['bofa_careers', 'upsjobs', 'verizoncareers', 'hersheycareers']
B_P = 0.01
H_PS = [0.8, 0.5]
NUM_RUNS = 5
DIV_WEIGHTS = [1.0, 0.8, 0.5, 0.2, 0.0]
GAMMAS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def get_path(network_name, b_p, h_p, div_weight, gamma, run_index):
    return (FIG_DATA_ROOT 
            + network_name
            + '/b_p_' + str(b_p)
            + '/h_p_' + str(h_p)
            + '/div_weight_' + str(div_weight)
            + '/gamma_' + str(gamma)
            + '/run_' + str(run_index) + '.json')
    
def get_csv():
    fig6_csv = open('./fig6_csv.csv', 'w')
    writer = csv.writer(fig6_csv, delimiter = ',')
    writer.writerow(['b_p', 
                     'network', 
                     'h_p', 
                     'lambda', 
                     'gamma', 
                     'run_index', 
                     'active_set', 
                     'majority'])
    for network_name in NETWORKS:
        for h_p in H_PS:
            for div_weight in DIV_WEIGHTS:
                for gamma in GAMMAS:
                    for run_index in range(5):
                        data = json.load(open(get_path(network_name, 
                                                       B_P, 
                                                       h_p, 
                                                       div_weight, 
                                                       gamma, 
                                                       run_index), 'r'))
                        writer.writerow([B_P, 
                                         network_name, 
                                         h_p, 
                                         div_weight, 
                                         gamma, 
                                         run_index, 
                                         data['active_set']['200'], 
                                         data['majority']['200']])
    fig6_csv.close()
    
if __name__ == '__main__':
    get_csv()