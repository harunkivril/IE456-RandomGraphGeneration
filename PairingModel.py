import argparse
import numpy as np
import utils
from random import shuffle


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


if __name__ == "__main__":
    # Get the arguments from command line and parse arguments here
    parser = argparse.ArgumentParser(description='Give required parametrs here')
    parser.add_argument('--input_path', required=True, type=str, help='Path of the input file')
    parser.add_argument('--output_folder', required=True, type=str, help='Path of the input file')
    parser.add_argument('--visualize', action='store_true', help='Path of the input file')
    args = parser.parse_args()
    input_file = args.input_path
    visualize = args.visualize
    output_folder = args.output_folder

    print("PAIRING MODEL")
    d = utils.read_input(input_file) #Read Input
    n_vertices = len(d)
    pairing_edges = pairing_model(d, limit_iterations=False) #Run algorithm
    print('EDGES: ', pairing_edges)
    if visualize:
        utils.visualize(pairing_edges, title="Pairing Model Graph Plot")
    
    input_index=input_file.split('/')[-1].split('-')[2] #Extract input index from input_file name
    output_file= output_folder + f'/O-13-{n_vertices}-{input_index}-PM.txt'
    utils.write_output(n_vertices, pairing_edges, output_file) #Save results
    