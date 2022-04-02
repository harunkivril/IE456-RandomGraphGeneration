import numpy as np
from time import time
import json
from HavelHakimi import havel_hakimi
from PairingModel import pairing_model
from SequentialAlgorithm import sequential_algorithm

#This is the script that we obtained our results. 

def generate_powerlaw_degreeseq(n_nodes, n=1.5):
    R = np.random.random(size=n_nodes) #Generate uniform random RVs
    X = (1/R)**(1/n) #Generate RVs from power law
    X = np.round(X) #Round the RVs to nearest integer

    return X

def generate_graphical_powerlaw_seqs(n_seqs=30, n_nodes=100):
    seqs = []
    while len(seqs) < n_seqs: # While there is not enough seq
        seq = generate_powerlaw_degreeseq(n_nodes) #Generate sequence
        seq = np.sort(np.array(seq, dtype=int))[::-1] #Sort vertices
        if havel_hakimi(seq.copy()): #Check graphicality
            seqs.append((seq))
    
    return seqs

edges = []
def compare_times(seqs):
    global edges
    results={}
    
    alg_start = time()
    for i , seq in enumerate(seqs):
        res = havel_hakimi(seq.copy())
        print(i, end=', ')
    results['Havel-Hakimi'] = {"total_time": time() - alg_start}
    
    failed = 0
    alg_start = time()
    for i, seq in enumerate(seqs):
        print(i, end=', ')
        res = pairing_model(seq.copy())
        if res is None:
            failed += 1
    results['Pairing Algorithm'] = {"total_time": time() - alg_start, "failed":failed}
    
    alg_start = time()
    for i, seq in enumerate(seqs):
        print(i, end=', ')
        res = sequential_algorithm(seq.copy())
    results['Sequential Algorithm'] = {"total_time": time() - alg_start}
    
    return results
    
if __name__ == "__main__":
    for i in (10, 20, 50, 100):
        print(i)
        sequences = generate_graphical_powerlaw_seqs(n_seqs=100, n_nodes=i) #Create 100 graphical sequences with i nodes
        results = compare_times(sequences) # Run algorithms for sequences
        results['sequences'] = [x.tolist() for x in sequences] #Make sequences as matrix
        with open(f'./experiment_n_{i}.json', 'w') as file: #Write results to json file
            json.dump(results, file)