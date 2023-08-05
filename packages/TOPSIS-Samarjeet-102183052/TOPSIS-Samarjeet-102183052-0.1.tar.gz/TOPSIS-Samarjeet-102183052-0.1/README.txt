Topsis Score and Rank calculator

'TOPSIS-Samarjeet-102183052' is a Python package implementing Multi-criteria decision making (MCDM) using Topsis. Topsis stands for Technique for Order of Preference by Similarity to Ideal Solution. 
Just provide your input attributes and it will give you the results


## Installation

$ pip install TOPSIS-102183052==0.1

In the commandline, you can write as -
    $ python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>

E.g for input data file as data.csv, command will be like
    $ python topsis.py input.csv "1,1,1,2" "+,+,-,+" output.csv

This will print all the output attribute values along with the Rank column, in a tabular format

License -> MIT