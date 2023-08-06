# TOPSIS

### What is TOPSIS?
Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) came in the 1980s as a multi-criteria-based decision-making (MCDM) method. TOPSIS chooses the alternative of shortest the Euclidean distance from the ideal solution and greatest distance from the negative ideal solution. 

___

## How to Install this Package?
``` pip install Topsis-Khushi-102183044 ```

___

## How to Run this Package?
``` topsis <inputFileName> <weights> <impacts> <resultFileName> ```

Eg. ``` topsis /Users/khushi/Desktop/102183044-data.csv "1,1,1,1,1" "+,+,-,+,+" /Users/khushi/Desktop/result.csv ```

___

## Constraints Applied
1. Number of parameters should be correct i.e. 5.
2. Print error message if input file doesn't exist.
3. The impacts and weights should be comma separated.
4. Impacts should only have +ve or -ve symbols.
5. Number of columns in the input csv file should be more or equal to 3.
6. The 2nd to last columns should be in numeric data type.
7. Number of weights, impacts and columns should be equal.

___

## Input File
| Fund Name  | P1 | P2 | P3 | P4 | P5  |
| ---------- | -- | -- | -- | -- | --  |
| M1         |0.75|0.56|6.3 |51.1|14.68|
| M2         |0.82|0.67|4.2 |41.2|11.72|
| M3         |0.89|0.79|6.5 |40.2|12.1 |
| M4         |0.92|0.85|5.8 |49.7|14.32|
| M6         |0.72|0.52|5.3 |61.1|16.91|
| M7         |0.69|0.48|3.6 |57.9|15.67|
| M8         |0.92|0.85|5.7 |31.2|9.67 |

___

## Output File
| Fund Name  | P1 | P2 | P3 | P4 | P5  | TOPSIS Score | Rank |
| ---------- | -- | -- | -- | -- | --- | ------------ | ---- |
| M1         |0.32|0.29|0.39|0.36|0.37 | 0.3655       | 8    |
| M2         |0.35|0.34|0.26|0.29|0.29 | 0.55         | 2    |
| M3         |0.38|0.41|0.41|0.28|0.30 | 0.48         | 5    |
| M4         |0.39|0.44|0.36|0.35|0.36 | 0.57         | 1    |
| M5         |0.33|0.30|0.41|0.39|0.39 | 0.39         | 7    |
| M6         |0.31|0.27|0.33|0.43|0.42 | 0.44         | 6    |
| M7         |0.29|0.25|0.22|0.41|0.39 | 0.50         | 4    |
| M8         |0.39|0.44|0.36|0.22|0.24 | 0.53         | 3    |

___

## License
MIT

___

## Written By
Name : Khushi Prasad
  
Roll No. : 102183044
