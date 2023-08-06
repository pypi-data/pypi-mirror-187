# Topsis
This is a python library which implements topsis.Topsis is a technique which is used for Multiple Criteria Decision Making(MCDM). It takes weights and impacts of criteria does the decision making by calculating the similarity to ideal solution.


## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package
```
pip install Topsis_Keshav_Garg_102017064
```


## Import

```
from Topsis_Keshav_Garg_102017064 import topsis
```

## Usage
topsis module has a function names get_score which takes 3 arguements as:
1. dataframe - It is a pandas dataframe which has atleast 3 columns(including the first column with names). It should only have numerical values. Any non-numerical value should be encoded before passing it to function.
2. weights - It is a string of comma(,) separated numbers which tell the weight of each criteria.
3. impacts - It is a string of comma(,) separated + and - sign showing the impact of criteria on decision making.

The function return the original pandas dataframe with 2 more columns added, which are Topsis Score and Rank.
```
topsis.get_score(dataframe,weights,impacts)
```


## Example

test.csv (Input):

|mobile|ram|memo|display|battery|price|
|------|---|----|-------|-------|-----|
|a|4|128|6.5|3500|15000|
|b|6|64|6.4|3800|16000|
|c|6|128|6.8|4200|19000|
|d|8|256|7|5000|25000|
|e|3|64|6.2|4000|14000|


```
from Topsis_Keshav_Garg_102017064 import topsis
import pandas as pd
df = pd.read_csv('./test.csv')
weights = "+,+,+,+,-"
impacts = "1,1,1,1,1"
print(topsis.get_score(df,weights,impacts))
```

Output:
|  |mobile|  ram|  memo|  display|  battery|  price|  Topsis Score|  Rank|
|--|------|----|--------|--------|-------|-------|----------|-------|
|0      |a    |4   |128    |6.5     |3500|  15000|     0.379477|     3|
|1      |b    |6   |64     |6.4     |3800|  16000|      0.341963|     4|
|2      |c    |6   |128    |6.8     |4200|  19000|      0.439078|     2|
|3      |d    |8   |256    |7.0     |5000|  25000|      0.729791|    1|
|4      |e    |3   |64     |6.2     |4000|  14000|      0.276912|     5|