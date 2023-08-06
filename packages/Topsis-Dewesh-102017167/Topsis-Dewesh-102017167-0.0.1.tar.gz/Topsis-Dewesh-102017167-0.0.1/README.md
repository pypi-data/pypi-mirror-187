# Topsis-Dewesh-102017167
## TOPSIS-PYTHON PACKAGE
## Introduction
Python Package for Multiple Criteria Decision Making using TOPSIS(Technique for Order of Preference by Similarity to Ideal Solution) Algorithm.
This is the part of the Assignment submitted by:
_Author: **Dewesh Agrawal**_
_Roll no: **102017167**_

## Installation and Usages:
<!-- Use the following code to install the package.-->
Run on the terminal:
```bash
pip install Topsis-Dewesh-102017167
```
Enter the parameters correctly as given below.Fristly, enter the inputfile with the .csv along with the weights and impacts values separated by commas, then enter the name of the file with .csv extension where you want to store the results.

```bash
sample: topsis <Inputfile><Weights><Impacts><outputfile>
```
Example: topsis data.csv "1,1,0.25,0.25" "+,-,+,-" outputfile.csv


## Topsis Algorithm:
### Step-01
Read the given dataset and create an evaluation matrix.

### Step-02
Normalize the matrix using the norm and the calculate the Multiply the normalised matrix with the Weights.

### Step-03
Determine the Ideal Best value and Ideal Worst value.
(-ve means minimum is best | +ve means maximum is best)

### Step-04
Calculate the Euclidean Distance from Ideal best and Ideal worst value.

### Step-05
Calculate the Perfromance Score.

### Step-06
Rank the alternatives based on the TOPSIS score.
