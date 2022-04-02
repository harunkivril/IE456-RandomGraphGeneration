The codes are written in python3 (3.8.3)
Required packages:
-numpy
-argparse
-matplotlib
-networkx
-json

The packages can be installed with pip:
    pip3 install <package_name>

The algorithms written seperately for easy reading however the submission accepts a single file therefor we combined all code into one script called IE456-13-Code.py
The seperated versions may be easier to use.

There is a python file for each algorithm each file takes 3 arguments, these algorithms also valid for combined script:
--input_path : The path of graph txt file
--output_folder : The folder that you want to save the results
--visualize : If this argument is given graphs are visualized.

Example call for combined script:
python3 IE456-13-Code.py --input_path ./Inputs/13-10-1-RandomComputer.txt --output_folder ./Outputs --visualize

Example call for seperately written code:
python3 PairingModel.py --input_path ./Inputs/13-10-1-RandomComputer.txt --output_folder ./Outputs --visualize
python3 HavelHakimi.py --input_path ./Inputs/13-10-1-RandomComputer.txt --output_folder ./Outputs --visualize
python3 SequentialAlgorithm.py --input_path ./Inputs/13-10-1-RandomComputer.txt --output_folder ./Outputs --visualize

If you would like to create random graphical sequences again as input CreateInputs.py can be used. It takes --input_folder as parameter.
python3 CreateInputs.py --input_folder ./Inputs

DegreeSeqGeneration.py is the script that we executed to construct results table. Also degree sequence generation functions are stored in this file.

utils.py is the file where the helper fuctions are defined

