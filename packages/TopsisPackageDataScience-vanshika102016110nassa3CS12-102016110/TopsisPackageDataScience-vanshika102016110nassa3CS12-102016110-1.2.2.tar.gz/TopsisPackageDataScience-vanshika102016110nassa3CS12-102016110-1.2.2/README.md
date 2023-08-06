# TOPSIS-Python

Submitted By: **Vanshika Nassa** <br>
Roll Number: **102016110** <br>
Batch: **3CS12**

***
git: <https://github.com/stuporunicorn/topsis102016110>
***

## Installation
```pip install TopsisPackageDataScience-vanshika102016110nassa3CS12-102016110```

## What is TOPSIS

**T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal
**S**olution (TOPSIS) originated in the 1980s as a multi-criteria decision
making method. TOPSIS chooses the alternative of shortest Euclidean distance
from the ideal solution, and greatest distance from the negative-ideal
solution. More details at [wikipedia](https://en.wikipedia.org/wiki/TOPSIS).

<br>

## How to use this package:

TopsisPackageDataScience-vanshika102016110nassa3CS12-102016110  can be run as in the following example:



### In Command Prompt
```
>> topsis data.csv "1,1,1,1,1" "+,-,+,-,+" result.csv
```
<br>



## Sample dataset

Consider this sample.csv file  

First column of file is removed by model before processing so follow the following format.  

All other columns of file should not contain any categorical values.

Fund Name,P1,P2,P3,P4,P5
M1,0.81,0.66,5.9,43.8,15.6
M2,0.67,0.58,1.8,62.1,16.4
M3,0.89,0.87,4.2,50.7,14.15
M4,0.82,0.67,2,32.6,11.98
M5,0.76,0.56,6.9,31.3,12.9
M6,0.72,0.88,2.7,47.8,12.8
M7,0.92,0.98,3.1,54.3,16.32
M8,0.78,0.61,7.1,36,10.85
weights vector = [0.25,1,1,0.80,1]

impacts vector = [ +,+,-,+,-]

### input:

```python
topsis sample.csv "0.25,1,1,0.80,1" "+,+,-,+,-" output.csv
```

### output:

output.csv file will contain following data :

Fund Name,P1,P2,P3,P4,P5,Topsis score,Rank
M1,0.81,0.66,5.9,43.8,15.6,0.25437487737312253,6
M2,0.67,0.58,1.8,62.1,16.4,0.6506396821452161,3
M3,0.89,0.87,4.2,50.7,14.15,0.5763040337448186,5
M4,0.82,0.67,2.0,32.6,11.98,0.6316539516437067,4
M5,0.76,0.56,6.9,31.3,12.9,0.1588440472634522,8
M6,0.72,0.88,2.7,47.8,12.8,0.7467977034332189,1
M7,0.92,0.98,3.1,54.3,16.32,0.6891413065596583,2
M8,0.78,0.61,7.1,36.0,10.85,0.23756825400098508,7


Information of benefit positive(+) or negative(-) impact criteria should be provided in `I`.

<br>

The rankings are stored in a csv file, with the 1st rank offering us the best decision, and last rank offering the worst decision making, according to TOPSIS method.

## Debugging and Exception Handling
> The program has several assert statements which raise errors with helpful description in the following cases:
> - Wrong dimensions of decision matrix (*not* 2D), weights (*not* 1D)
> - Length of weights and impacts don't match 
> - Weights or impacts don't match number of attributes
> - For command line, number of arguments is less than 3 required
> - File extension must be .csv

## License
Copyright 2023 Vanshika Nassa
<br>
This repository is licensed under the MIT license.
<br>
See LICENSE for details.
[MIT](https://choosealicense.com/licenses/mit/)