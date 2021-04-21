import csv
import json

FIG_DATA_ROOT = './fig_data/'
NETWORKS = ['bofa_careers', 'upsjobs', 'verizoncareers', 'hersheycareers']
B_P = 0.01
H_PS = [0.8, 0.5]
NUM_RUNS = 5
THRESHOLD_DEV = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]


def get_path(network_name, b_p, h_p, run_index):
    return (FIG_DATA_ROOT 
            + network_name
            + '/b_p_' + str(b_p)
            + '/h_p_' + str(h_p)
            + '/run_' + str(run_index) + '.json')

def get_csv():
    fig7_csv = open('./fig7_csv.csv', 'w')
    writer = csv.writer(fig7_csv, delimiter = ',')
    writer.writerow(['b_p', 
                     'network', 
                     'h_p', 
                     'offset', 
                     'run_index', 
                     'active_set', 
                     'majority'])
    for network_name in NETWORKS:
        for h_p in H_PS:
            for dev in THRESHOLD_DEV:
                for run_index in range(NUM_RUNS):
                    data = json.load(open(get_path(network_name, B_P, h_p, run_index), 'r'))
                    writer.writerow([B_P, 
                                     network_name, 
                                     h_p, dev, 
                                     run_index, 
                                     data[str(dev)]['active_set'], 
                                     data[str(dev)]['majority']])
    fig7_csv.close()
    
if __name__ == '__main__':
    get_csv()