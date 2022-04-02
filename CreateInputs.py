from DegreeSeqGeneration import generate_graphical_powerlaw_seqs
from utils import write_input
import argparse

#Take parameters from the command line
parser = argparse.ArgumentParser(description='Give required parameters here')
parser.add_argument('--input_folder', required=True, type=str, help='Input folder to store rxts')
args = parser.parse_args()
INPUTS_PATH = args.input_folder

# Create random instances from power law with 10,20,50 with 5 from each
i=1
n_instances = 5
for n_nodes in (10, 20, 50):
    sequences = generate_graphical_powerlaw_seqs(n_seqs=n_instances,n_nodes=n_nodes)
    for sequence in sequences:
        save_name = INPUTS_PATH + f'/13-{n_nodes}-{i}-RandomComputer.txt'
        write_input(save_name, sequence)
        i += 1
