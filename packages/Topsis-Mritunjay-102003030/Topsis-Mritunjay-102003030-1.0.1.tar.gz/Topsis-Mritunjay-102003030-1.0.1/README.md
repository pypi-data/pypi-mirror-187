# TOPSIS SCORE CALCULATOR
By: **MRITUNJAY-102003030**

### Title: Multiple Criteria Decision Making(MCDM) Using TOPSIS

## WHAT IS TOPSIS
TOPSIS is an acronym that stands for 'Technique of Order Preference Similarity to the Ideal Solution' and is a pretty straightforward MCDA method.
This is a Python library for dealing with Multiple Criteria Decision Making(MCDM) problems by using Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS).

#### HOW TO INSTALL THE TOPSIS PACKAGE
```buildoutcfg
pip install Topsis-Mritunjay-102003030
```

#### FOR CALCULATING THE TOPSIS SCORE
```buildoutcfg
Topsis data.csv "0.25,0.25,0.25,0.25" "+,+,-,+" result.csv
```

##### Input File(Example:data.csv):
Argument used to pass the path of the input file which conatins a dataset having different fields and to perform the topsis mathematical operations
##### Weights(Example:"0.25,0.25,0.25,0.25")
The weights to assigned to the different parameters in the dataset should be passed in the argument.**It must be seperated by ','.**
##### Impacts(Example:"+,+,-,+"):
The impacts are passed to consider which parameters have a positive impact on the decision and which one have the negative impact.**Only '+' and '-' values should be passed and should be seperated with ',' only**
##### Output File(Example:result.csv):
This argument is used to pass the path of the result file where we want the rank and score to be stored.

## EXAMPLE

#### data.csv

A csv file showing data for different mobile handsets having varying features.

| Model  | Storage space(in gb) | Camera(in MP)| Price(in $)  | Looks(out of 5) |
| :----: |:--------------------:|:------------:|:------------:|:---------------:|
| M1 | 16 | 12 | 250 | 5 |
| M2 | 16 | 8  | 200 | 3 |
| M3 | 32 | 16 | 300 | 4 |
| M4 | 32 | 8  | 275 | 4 |
| M5 | 16 | 16 | 225 | 2 |

weights vector = [ 0.25 , 0.25 , 0.25 , 0.25 ]

impacts vector = [ + , + , - , + ]

### INPUT:

```python
topsis data.csv "0.25,0.25,0.25,0.25" "+,+,-,+" result.csv
```

### OUTPUT:
```
      TOPSIS RESULTS
-----------------------------

    P-Score  Rank
1  0.534277     3
2  0.308368     5
3  0.691632     1
4  0.534737     2
5  0.401046     4

``` 

