# Topsis
TOPSIS is based on the fundamental premise that the best solution has the shortest distance from the positive-ideal solution, and the longest distance from the negative-ideal one. Alternatives are ranked with the use of an overall index calculated based on the distances from the ideal solutions.

It takes 4 arguments :
1.Data.csv file
2.Weights
3.Impacts
4.Result file

Returns file with Ranks and Topsis Score

## How to use it?
Open terminal and type topsis data file name weights impacts result file name

ex: topsis data.csv 1,1,1,1 +,+,-,+ resullt.csv