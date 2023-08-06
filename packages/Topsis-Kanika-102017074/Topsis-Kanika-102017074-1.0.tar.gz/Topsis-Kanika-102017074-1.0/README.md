# Topsis-kanika-102017074

Topsis-kanika-102017074 is a Python package that provides an implementation of the Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) method for multi-criteria decision making. 

## Installation
You can install Topsis-kanika-102017074 using pip by running the following command:
pip install Topsis-kanika-102017074


## Usage
```python
from topsis import topsis

weights = [1, 1, 1, 1, 1]
impacts = ["+", "-", "+", "-", "+"]
#data=[data.csv]

result = topsis(weights, impacts, data)

## Inputs
The function takes three inputs:

weights : list of weights assigned to each criteria
impacts : list of signs assigned to each criteria, either '+' or '-'
data : a 2D list of the decision matrix where the first column contains the names of the alternatives and the rest of the columns contain the criteria values.

# Output
The function returns a 2D list of the decision matrix along with two additional columns for Topsis score and rank respectively.

# Note
The number of weights, impacts and columns in the decision matrix should be same.
Impacts should be either '+' or '-'.