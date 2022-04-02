import utils
import numpy as np
import argparse
from random import shuffle, seed

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


if __name__ == "__main__":
    # Take parameters from command line and parse
    parser = argparse.ArgumentParser(description='Give required parametrs here')
    parser.add_argument('--input_path', required=True, type=str, help='Path of the input file')
    parser.add_argument('--output_folder', required=True, type=str, help='Path of the input file')
    parser.add_argument('--visualize', action='store_true', help='Path of the input file')
    args = parser.parse_args()
    input_file = args.input_path
    visualize = args.visualize
    output_folder = args.output_folder

    print('HAVEL-HAKIMI')
    edges = []
    d = utils.read_input(input_file) #Read input
    n_vertices = len(d)
    print('Is graphical: ', havel_hakimi(d, construct_graph = True)) #Execute algorithm
    print('Edges:', edges)
    if visualize:
        utils.visualize(edges, title="Havel-Hakimi Graph Plot")
    
    input_index=input_file.split('/')[-1].split('-')[2] #Extract input index from input_file name
    output_file= output_folder + f'/O-13-{n_vertices}-{input_index}-HH.txt'
    utils.write_output(n_vertices, edges, output_file) #Save output
    