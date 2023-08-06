# TOPSIS

## Goals of this project :
- Learn about mathematics of TOPSIS Algorithm
- Implementation of TOPSIS Algorithm using python. The code for same is available in 102017187.py file
- Create a package and publish it on (https://pypi.org/). Also, provide a user manual for it.
- Test the package by installing it and run it through command line.
- Create a web app for TOPSIS

-------------------------

### What is TOPSIS ? 
- Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria-based decision-making method 
- {Eg. You want to purchase a mobile phone. But you are confused because there are so many factors like price, memory, battery, camera quality etc. So, TOPSIS provides you the solution.} 
- It is a way to allocate the ranks on basis of the weights and impact of the given factors.

-------------------------

### How to install this package ?
On command prompt type :
`pip install Topsis-Jasween-102017187`
(along with version, copy it from top left corner under package name)
-------------------------

### Example of how to use it on command line:
<br>
On command prompt type :
Usages: `topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>`
eg. `topsis C:\Users\username\Downloads\102017187-data.csv "1,1,1,1,1" "+,-,+,-,+" C:\Users\username\Downloads\resultant.csv`

**Parameters:**
| Arguments | Description |
| --- | --- |
| InputDataFile | Input CSV file path |
| Weights | Comma separated numbers |
| Impacts | Comma separated either '+' or '-' |
| ResultFileName | Output CSV file path |

---------------------- 

 -It accepts input file (which contains parameters and their values in csv format) and weights and impacts.
- It creates a output file(.csv), that contains the original data with Topsis Score and Ranks.

------------------------

Sample Input File

| Fund Name | P1 | P2 | P3 | P4 | P5 |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | 0.94 | 0.88 | 5.6 | 34.9 | 10.58 | 
| M2 | 0.94 | 0.88 | 4.5 | 32.7 | 9.76 | 
| M3 | 0.74 | 0.55 | 4.4 | 57.8 | 15.87 |
| M4 | 0.60 | 0.36 | 5.0 | 63.0 | 17.24 | 
| M5 | 0.61 | 0.37 | 3.4 | 65.3 | 17.42 | 
| M6 | 0.74 | 0.55 | 6.9 | 44.4 | 13.15 | 
| M7 | 0.65 | 0.42 | 5.4 | 62.9 | 17.34 | 
| M8 | 0.63 | 0.40 | 7.0 | 64.5 | 18.13 | 

-----------------------------------------------

Sample Output File: 

| Fund Name | P1 | P2 | P3 | P4 | P5 | Topsis Score | Rank |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | 0.94 | 0.88 | 5.6 | 34.9 | 10.58 | 0.441618 | 7 |
| M2 | 0.94 | 0.88 | 4.5 | 32.7 | 9.76 | 0.405738 | 8 |
| M3 | 0.74 | 0.55 | 4.4 | 57.8 | 15.87 | 0.48147 | 6 |
| M4 | 0.60 | 0.36 | 5.0 | 63.0 | 17.24 | 0.565738 | 4 |
| M5 | 0.61 | 0.37 | 3.4 | 65.3 | 17.42 | 0.500978 | 5 |
| M6 | 0.74 | 0.55 | 6.9 | 44.4 | 13.15 | 0.631272 | 1 |
| M7 | 0.65 | 0.42 | 5.4 | 62.9 | 17.34 | 0.572967 | 3 |
| M8 | 0.63 | 0.40 | 7.0 | 64.5 | 18.13 | 0.623423 | 2 |

-------------------------

### Be careful about these, otherwise you will get an error :smile: :
- Correct no. of parameters must be provided in command line
- Input file must be in csv format and must be present
- Input file must contain three or more columns
- Input file: first column is the object/variable name (e.g. M1, M2, M3, M4…...)
- Input file: from 2nd to last column the valuse should be only numeric
- Result file should be .csv file
- Weights and impacts should be in correct format and separated by ","
- Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.
- Impacts must be either +ve or -ve

-------------------------



