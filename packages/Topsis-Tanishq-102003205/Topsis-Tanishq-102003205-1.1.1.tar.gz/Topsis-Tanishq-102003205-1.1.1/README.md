# Topsis-Tanishq-102003205
Topsis analysis of a csv file in python


## About Topsis

It is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion. An assumption of TOPSIS is that the criteria are monotonically increasing or decreasing. Normalisation is usually required as the parameters or criteria are often of incongruous dimensions in multi-criteria problems.

## Installation


```bash
pip install Topsis-Tanishq-102003205
```

## Usage

Enter csv filename followed by .csv extentsion, then enter the weights vector with vector values separated by commas, followed by the impacts vector with comma separated signs (+,-).

```
topsis 102003205-data.csv "1,1,1,1,1" "+,+,+,+,+" output.csv

```

Rank 1 signifies best decision.


## Other
The csv file (from 2nd column to last column) should not contain non-numeric values.
The first column and first row are dropped in processing the data.


## License
©  2023 Tanishq Singla
[MIT](https://choosealicense.com/licenses/mit/)
