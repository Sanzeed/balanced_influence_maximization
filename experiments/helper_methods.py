import json
import networkx as nx


def calculate_majority(graph):
    category_count = {}
    
    for node in graph.nodes():
        node_label = graph.node[node]['label']
        category_count[node_label] = category_count.get(node_label, 0) + 1
    
    return max(category_count, key = lambda category : category_count[category])

def calculate_theta(graph):
    e_same, e_diff = 0, 0
    
    for (u, v) in graph.edges():
        if graph.node[u]['label'] == graph.node[v]['label']:
            e_same += 1
        else:
            e_diff += 1
            
    return e_same / e_diff
    
def get_homophilic_diffusion_probability(graph, u, v, theta, b_p, h_p):
    if graph.node[u]['label'] == graph.node[v]['label']:
        h_e = h_p
    else:
        h_e = 1 - h_p
        
    return (1 + theta) * h_e * b_p / (1 - h_p + h_p * theta)
    
def fetch_graph(graph_path):    
    with open(graph_path, 'r') as graph_file:
        graph_data = json.load(graph_file)
        
    edges = graph_data["edges"]
    labels = {int(node_str) : {'label' : graph_data["labels"][node_str]}
              for node_str in graph_data["labels"]}
    
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    nx.set_node_attributes(graph, labels)
    
    return graph
