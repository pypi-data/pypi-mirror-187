

_for: **Topsis_Cherish_102003647**_
_submitted by: **Cherish Mahajan**_
_Roll no: **102003647**_
_Group: **3COE25**_


Topsis_Cherish_102003647 is a Python library for solving Multiple Criteria Decision Making(MCDM) problems by  Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Topsis-Cherish-102003647.

```bash
pip install Topsis_Cherish_102003647
```

## Usage

Enter csv filename followed by _.csv_ extension, then enter the _weights_ vector with vector values separated by commas, followed by the _impacts_ vector with comma separated signs _(+,-)_

### Input
And using this package in Python as :
```bash
import topsispy as tp
a =[
     [250, 16, 12, 5],
     [200, 16, 8, 3],
     [300, 32, 16, 4],
     [275, 32, 8, 4],
     [225, 16, 16, 2]
   ]
w = [0.25, 0.25, 0.25, 0.25]
sign = [-1, 1, 1, 1]
tp.topsis(a, w, sign)
```

The package can be used via commandline as :
``` bash
$ python [package name] [path of csv as string] [list of weights as string] [list of sign as string]
```
## Example

#### sample.csv

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



### Output:

      TOPSIS RESULTS
      As per the given sample, the output file looks as given below :


| Model  | Storage space(in gb) | Camera(in MP)| Price(in $)  | Looks(out of 5) |Topsis Score  |  Rank  |
| :----: |:--------------------:|:------------:|:------------:|:---------------:|:------------:|:------:|
| M1 | 16 | 12 | 250 | 5 | 0.534277 | 3 |
| M2 | 16 | 8  | 200 | 3 | 0.308368 | 5 |
| M3 | 32 | 16 | 300 | 4 | 0.691632 | 1 |
| M4 | 32 | 8  | 275 | 4 | 0.534737 | 2 |
| M5 | 16 | 16 | 225 | 2 | 0.401046 | 4 |
   


## Other notes

* The first column and first row have only been omitted by the library Topsis-Cherish-102003647 before processing, in attempt to remove indices and headers. So make sure the csv follows the format as shown in sample.csv otherwise the code will have issues in working properly.
* Make sure the csv does not contain categorical values since the code takes into account all the values which are encoded as numerical values.
* The Topsis-Cherish-102003647 works on the sample data and calculates the topsis score according to which it provides the rank to each available option.

