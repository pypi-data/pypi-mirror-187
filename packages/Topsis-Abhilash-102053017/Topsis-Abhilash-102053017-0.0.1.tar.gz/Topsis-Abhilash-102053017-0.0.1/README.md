#Topsis-Abhilash-102053017
## Topsis Package



This package lets user enter an input file and then generated an output into a corresponding output file wherein the items are given a rank on the basis of weight and impact entered by the user

Used for multi-criteria decision analysis.

TOPSIS stands for Technique for Order of Preference by Similarity to Ideal Solution

Just provide the input attributes and it will gives the results

## Features
-checks for input and output file errors

## Installation

Install the dependencies and devDependencies and start the server.

```sh
$ pip install Topsis-Abhilash-102053017

$ python <package_name> <path to input_data_file_name> <weights as strings> <impacts as strings> <result_file_name>

E.g for input data file as data.csv:
$ python topsis.py data.csv "1,1,1,1" "+,+,-,+" output.csv

This will print all the output attribute values along with the rank column, in a tabular format
```

