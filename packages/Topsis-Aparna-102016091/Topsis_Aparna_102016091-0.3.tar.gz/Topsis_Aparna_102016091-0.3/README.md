Submitted By: Aparna Sood

## What is TOPSIS?

Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.

It is a package for Multiple-criteria decision-making using TOPSIS. Requires input file,weights and impacts. Returns a data frame which has score and rank of every label. This package helps improve decision-making.

## Installation
```sh
pip install Topsis-Aparna-102016091
```

## Usage

```sh
import Topsis_Aparna_102016091 as ap 
ap.topsisscore(inputfilename.csv , weights , impacts , outputfilename.csv)
```
- weights and impacts provided as parameters should be separated by comma(,) and equal to number of columns.
- weights should only contain numeric values
- the categorical column should either be dropped or enginnered into a numerical column

Take care of these and you are ready to go.

## Result

The output (outputfilename.csv) is saved as csv file, with extra two columns of topsis score and rank.
Rank 1 signifies best decision.
## Contribution

Pull requests are welcome!!

## Example

inputfilename.csv

|Fund Name|P1  |P2  |P3 |P4  |P5   |
|---------|----|----|---|----|-----|
|M1       |0.8 |0.64|6.9|44.5|13.21|
|M2       |0.81|0.66|7  |33.1|10.39|
|M3       |0.89|0.79|4.1|49.1|13.72|
|M4       |0.8 |0.64|4.8|45.1|12.84|
|M5       |0.79|0.62|7  |65.1|18.38|
|M6       |0.8 |0.64|4.1|51.2|14.19|
|M7       |0.61|0.37|4.2|48  |13.3 |
|M8       |0.71|0.5 |4.1|43.1|12.1 |

weights = "1,1,1,1,1"

impacts = "+,-,+,-,+"

outputfilename.csv 

|FIELD1|Fund Name|P1  |P2 |P3  |P4   |P5   |topsis score       |rank|
|------|---------|----|---|----|-----|-----|-------------------|----|
|0     |M1       |0.8 |0.64|6.9 |44.5 |13.21|0.5513405258358909 |1.0 |
|1     |M2       |0.81|0.66|7.0 |33.1 |10.39|0.5474324527004779 |2.0 |
|2     |M3       |0.89|0.79|4.1 |49.1 |13.72|0.356585782293044  |8.0 |
|3     |M4       |0.8 |0.64|4.8 |45.1 |12.84|0.4305717292651279 |6.0 |
|4     |M5       |0.79|0.62|7.0 |65.1 |18.38|0.5240978466600755 |3.0 |
|5     |M6       |0.8 |0.64|4.1 |51.2 |14.19|0.38297613208032333|7.0 |
|6     |M7       |0.61|0.37|4.2 |48.0 |13.3 |0.5010998980377374 |4.0 |
|7     |M8       |0.71|0.5|4.1 |43.1 |12.1 |0.45991281671067175|5.0 |



