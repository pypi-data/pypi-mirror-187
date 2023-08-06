
**Name** - Shikha
**Roll no.** - 102016009


## Installation


```bash
pip install 102016009-topsis
```

## Usage

Following query on terminal will provide you the topsis analysis for input csv file.

```
102016009-topsis -n "dataset-name.csv" -w "w1,w2,w3,w4,..." -i "i1,i2,i3,i4,..."

```

w1,w2,w3,w4 represent weights, and i1,i2,i3,i4 represent impacts where 1 is used for maximize and 0 for minimize. 
Size of w and i is equal to number of features. 

Note that the first row and first column of dataset is dropped

Rank 1 signifies best decision



MIT