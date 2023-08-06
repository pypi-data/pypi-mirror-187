# Topsis-Ayesha-102197019
Hello there!This module will help you compute the TOPSIS Score and Ranking for your MCDM
(Multiple Criteria Decision making) problems

## Installation
```pip install Topsis-Ayesha-102197019```

## How to use it?
Open your terminal and ensure you have pandas and numpy packages installed if not please install them using:
```pip install pandas```

Once this is done type Topsis and give the following command line arguments
1.The input data file
2.The weights for the column feature
3.The impoact for each each column feature
4.The result csv file to store the result in

Usages: Topsis <InputDataFilePath> <Weights> <Impacts> <ResultFileNamePath> Example: python Ex:
```Topsis /Users/abc/Desktop/data.csv “1,1,1,2,2” “+,-,+,-,+” /Users/abc/Desktop/res.csv``


Usage Notes:
• Correct number of parameters must be entered(inputFileName, Weights, Impacts, resultFileName)

• Input file must contain three or more columns.

• From 2nd to last columns must contain numeric values only 

• Number of weights, number of impacts and number of columns (from 2nd to last columns) must
be same.

• Impacts must be either +ve or -ve.

• Impacts and weights must be separated by ‘,’ (comma).

## License

This repository is licensed under the MIT license.See LICENSE for details

