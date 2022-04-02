from HavelHakimi import havel_hakimi
import numpy as np
import argparse
import utils


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
    # Get arguments from command line and parse arguments
    parser = argparse.ArgumentParser(description='Give required parameters here')
    parser.add_argument('--input_path', required=True, type=str, help='Path of the input file')
    parser.add_argument('--output_folder', required=True, type=str, help='Path of the input file')
    parser.add_argument('--visualize', action='store_true', help='Path of the input file')
    args = parser.parse_args()
    input_file = args.input_path
    visualize = args.visualize
    output_folder = args.output_folder

    print("Sequential Algorithm")
    d = utils.read_input(input_file) #Read input file
    n_vertices = len(d)
    sequential_edges = sequential_algorithm(d) #Run algorithm
    print("EDGES: ", sequential_edges)
    if visualize:
        utils.visualize(sequential_edges, title="Sequential Algorithm Graph Plot")
    
    input_index=input_file.split('/')[-1].split('-')[2] #Extract input index from input_file name
    output_file= output_folder + f'/O-13-{n_vertices}-{input_index}-SA.txt'
    utils.write_output(n_vertices, sequential_edges, output_file) #Save output
    