### Topsis_102003634

_for: **Topsis_102003634**_
_submitted by: **Falguni Sharma**_
_Roll no: **102003634**_
_Group: **3COE25**_


Topsis_102003634 is a Python library for solving Multiple Criteria Decision Making(MCDM) problems by  Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS). This package works on both string values as well as float values.

For attributes which are string type, the following table is used.

    low                     1
    below average           2
    average                 3
    good                    4
    excellent               5

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Topsis_102003634.

```bash
pip install Topsis_102003634
```

## Usage

Enter csv filename followed by _.csv_ extension, then enter the _weights_ vector with vector values separated by commas, followed by the _impacts_ vector with comma separated signs _(+,-)_ both enclosed within "" and then at the end write the output file name.

### Input


The package can be used via commandline as :
``` bash
$ python <package name> <path of csv as string> "<list of weights as string>" "<list of sign as string>" <output file name>
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
   


