import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def read_input(txt_path):
    degree_sequence = []
    with open(txt_path, 'r') as file:
        for i, line in enumerate(file):
            if i >0:
                degree_sequence.append(int(line))
    return np.array(degree_sequence)

def write_input(txt_path, degree_sequence):
    n_vertices = len(degree_sequence)
    with open(txt_path, 'w') as file:
        file.write(f'{n_vertices}\n')
        for d in degree_sequence:
            file.write(f'{d}\n')

def write_output(n_vertices, edges, save_path):
    if edges is not None:
        with open(save_path, 'w') as file:
            file.write(f'{n_vertices}\n')
            for edge in edges:
                file.write(f'{edge[0]} {edge[1]}\n')
    else:
         with open(save_path, 'w') as file:
            file.write(f'0\n')

def visualize(edge_list, title='Graph'):
    G = nx.Graph() #Init graph
    G.add_edges_from(edge_list) #Addd eddges to graph
    plt.title(title) #Set graph title
    nx.draw(G, with_labels=True, font_weight='bold') #Draw graph
    plt.show()