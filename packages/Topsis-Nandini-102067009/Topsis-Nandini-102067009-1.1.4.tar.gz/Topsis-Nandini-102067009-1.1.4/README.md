# Topsis Package (API & CLI)

> CLI scripts takes `csv/excel` files as input!

## Installation
```
pip install Topsis-Nandini-102067009
```

## Command Line Usage
```
topsis input_file weights impacts output_file
```
### Arguments
| Arguments | Description |
|------------| -----------------|
| input_file |  "CSV/Excel" file path |
| weights | Comma separated numbers |
| impacts | Comma separated '+' or '-' |
| output_file | Output CSV file path |

### Output
Creates a *output_file*, that contains the original data with performance score and rank.

Example:
```bash
topsis data.xlsx "1,1,1,1,1" "+,-,+,-,+" output.csv 
```

## API Usage
### Steps
1. Import topsis function from module topsis
2. Invoke topsis function by passing in data, weights, impacts

Example:
```python
from topsis import topsis
import pandas as pd

df = pd.read_csv('data.csv')
weights = [2,2,3,3,4]
impacts=[1,-1,1,-1,1]
print(topsis(df, weights, impacts))
```

