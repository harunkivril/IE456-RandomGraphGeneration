import utils
import numpy as np
import argparse
from random import shuffle, seed
import networkx as nx
import matplotlib.pyplot as plt


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


def add_edges(di, vertex_id, vertex_ids):
    global edges
    for i in range(di):
        edges.append((vertex_id, vertex_ids[i]))

def havel_hakimi(d:list, vertex_ids:list=None, construct_graph=False) -> bool:
    """
    d: sorted descendingly and degree >= 0:list
    vertex_ids: Id of the vertices can be specified before or the function will assing ids
    Requires a return_graph:bool and empty edges:list if return_grah is True.
    """
    if vertex_ids is None: #Set vertex ids to construct the graph
        vertex_ids = np.array(range(1,len(d)+1))
    
    if sum(d) == 0: #if d all zeros
        return True
    
    di = d[0]  #Since d always sorted i=0
    d = d[1:] #Remove di from d
    vertex_id = vertex_ids[0] #Get vertex id
    vertex_ids = vertex_ids[1:] #Remove ith vertex from vertex_ids
    
    if sum(d > 0) < di: #If there is not enough positive vertices
        if construct_graph:
            global edges
            edges = None #Return None for edges if graph is not realizable
        return False
    
    d[:di] += -1 #Remove edges between selected and others
    
    if construct_graph:
        add_edges(di,vertex_id, vertex_ids)
        
    idx = np.argsort(d)[::-1] #sorted indices of d
    d = d[idx] #Sort d using indices
    vertex_ids = vertex_ids[idx] #Also sort vertex_ids to match new d
    
    return havel_hakimi(d, vertex_ids, construct_graph)

def check_simplicity(edges):
    edges = np.array(edges)
    # Make smaller vertice id appear first to compare easily
    edges = np.sort(edges, axis=1)

    # Check if is there any loops
    for edge1 in edges:
        if edge1[0] == edge1[1]:
            return False

    # Check if any multiple edges
    # Looping in python is slow. I prefer numpy functions works on lower level.
    if len(edges) > len(np.unique(edges, axis=0)):
        return False

    return True

def pairing_model(d, limit_iterations=True):
    '''
    d: graphical degree sequence
    '''
    # Raise error if accidentaly improper seq is passed.
    if sum(d) % 2 == 1:
        raise ValueError('Sum of degrees are odd.')
    if max(d) >= len(d):
        raise ValueError('There is a degree with di > n_vertices-1')

    is_simple = False

    cells = []
    for i in range(1, len(d)+1):  # for every degree of every vertex add a one sided edge to cells
        # 3*[1] = [1,1,1] in python and [1,1] + [1] = [1,1,1]
        cells = cells + d[i-1]*[i]

    n_edges = int(sum(d)/2)
    
    trials = 0
    while not is_simple:  # Until a simple graph is obtained
        if trials % 10000 == 0:
            print("", end=f"\rTrial: {trials}")
        #print('Trial: {}'.format(trials), end='\r')
        shuffle(cells)  # Shuffle cells
        # match first half and the second to obtain edges
        edges = list(zip(cells[:n_edges], cells[n_edges:]))
        # check if edges construct a simple graph
        is_simple = check_simplicity(edges)
        trials += 1
        
        if trials > 1e6+1 and limit_iterations: # 1M iteration limit
            print('\nWARNING: ITERATION LIMIT EXCEDEED')
            return None
    print('\n')
    return edges

def sequential_algorithm(d):
    """
    d: Graphical degree seq.
    """
    edges = []
    # If all zero we are done
    if sum(d) == 0:
        return edges
    
    #Select i with minimal positive entry by replacing negatives with infinity
    idx = np.where(d > 0, d, np.inf).argmin()
    
    # While degree of i is not zero
    while d[idx] > 0:
        prob_weights=[]
        J=[]
        # Create candidate list
        for j in range(len(d)):
            #j not equal to i and no negative degrees allowed and the candidate not in edges
            if j != idx and d[j] > 0 and ((idx,j) not in edges or (j,idx) not in edges):
                d_temp = d.copy()
                d_temp[j] = d_temp[j]-1 #remove 1 from j
                d_temp[idx] = d_temp[idx]-1 #remove 1 from i
                d_temp[::-1].sort() # sort d_temp for havel-hakimi
                if havel_hakimi(d_temp): #Is candidate graphical?
                    J.append((idx+1,j+1)) #Add candidate to candidate list
                    prob_weights.append(d[j]) #Add its degree to prob weights
        
        probs = np.array(prob_weights)/sum(prob_weights) #Convert weights to probs
        selected_idx = np.random.choice(list(range(len(J))), size=1, p=probs)[0] #Select an edge with given probs
        selected_edge = J[selected_idx]
        edges.append(selected_edge) #Add selected edge to edges
        d[idx] =  d[idx]-1 #Remove 1 from i
        j = selected_edge[1] -1 #Since 
        d[j] = d[j] - 1 #Remove 1 from j
    
    return sequential_algorithm(d) + edges #Return step 2

if __name__ == "__main__":
    # Get the arguments from command line and parse arguments here
    parser = argparse.ArgumentParser(description='Give required parametrs here')
    parser.add_argument('--input_path', required=True, type=str, help='Path of the input file')
    parser.add_argument('--output_folder', required=True, type=str, help='Path of the input file')
    parser.add_argument('--visualize', action='store_true', help='Path of the input file')
    args = parser.parse_args()
    input_file = args.input_path
    visualize_graphs = args.visualize
    output_folder = args.output_folder

    d = read_input(input_file) #Read input
    n_vertices = len(d)
    input_index=input_file.split('/')[-1].split('-')[2] #Extract input index from input_file name

    # Run Havel-Hakimi
    print('HAVEL-HAKIMI')
    edges = []
    is_graphical = havel_hakimi(d.copy(), construct_graph = True)
    print('Is graphical: ', is_graphical) #Execute algorithm
    print('Edges:', edges)
    if visualize_graphs:
        visualize(edges, title="Havel-Hakimi Graph Plot")
    
    output_file= output_folder + f'/O-13-{n_vertices}-{input_index}-HH.txt'
    write_output(n_vertices, edges, output_file) #Save output

    # Run Pairing Model
    print("PAIRING MODEL")
    if is_graphical:
        pairing_edges = pairing_model(d, limit_iterations=False) #Run algorithm
        print('EDGES: ', pairing_edges)
        if visualize_graphs:
            visualize(pairing_edges, title="Pairing Model Graph Plot")
    else:
        pairing_edges = None
    
    output_file= output_folder + f'/O-13-{n_vertices}-{input_index}-PM.txt'
    write_output(n_vertices, pairing_edges, output_file) #Save results

    # Run Sequential Algorithm
    print("SEQUENTIAL ALGORITHM")
    if is_graphical:
        sequential_edges = sequential_algorithm(d) #Run algorithm
        print("EDGES: ", sequential_edges)
        if visualize_graphs:
            visualize(sequential_edges, title="Sequential Algorithm Graph Plot")
        
        output_file= output_folder + f'/O-13-{n_vertices}-{input_index}-SA.txt'
    else:
        sequential_edges = None
    write_output(n_vertices, sequential_edges, output_file) #Save output