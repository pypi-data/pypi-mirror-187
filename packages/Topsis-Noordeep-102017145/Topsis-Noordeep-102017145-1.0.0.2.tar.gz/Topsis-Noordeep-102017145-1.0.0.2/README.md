# Topsis-Noordeep-102017145
Topsis-Noordeep-102017145 is a Python package for dealing with Multiple Criteria Decision Making(MCDM) problems by using Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS).
Topsis is a method of compensatory aggregation that compares a set of alternatives, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion.

#### Installation
```
Use the package manager pip to install Topsis-Noordeep-102017145
```
#### Syntax
```
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>
Example:
topsis inputfile.csv 1,2,1,2,1 +,+,-,+,- result.csv
```
#### Example
Sample Input Data
| Name | P1 | P2 | P3 | P4 | P5 |
| --- | --- | --- | --- | --- | --- |
| M1 | 0.71 |0.5|3.8|40.8|11.5|
| M2 | 0.94 | 0.88| 5.3|56.2 |15.83 |
| M3 |0.85 |0.72|4 |30.5 |9.02 |
| M4 |0.61  |0.37|5.4 |56.9 |15.82 |
| M5 |0.91 |0.83|3.4 |53.4 |14.64 |

Weights: 1,1,1,1,1
Impacts: +,+,+,+,+

Sample Output Data
| Name | P1 | P2 | P3 | P4 | P5 |Score|Rank|
| --- | --- | --- | --- | --- | --- |---|---|
| M1 | 0.71 |0.5|3.8|40.8|11.5|0.3015751942839768|5|
| M2 | 0.94 | 0.88| 5.3|56.2 |15.83 |0.97815026808521971|1
| M3 |0.85 |0.72|4 |30.5 |9.02 |0.4172925776259159|4
| M4 |0.61  |0.37|5.4 |56.9 |15.82 |0.5053936295885693|3
| M5 |0.91 |0.83|3.4 |53.4 |14.64 |0.6774035368116197|2

#### Note
1. Enter the path of your input csv file.
2. Enter the weights and impacts vector with each entry separated by commas.
3. Enter the name of output file in .csv format.
4. The Output file will be created in the current working directory

### License
MIT