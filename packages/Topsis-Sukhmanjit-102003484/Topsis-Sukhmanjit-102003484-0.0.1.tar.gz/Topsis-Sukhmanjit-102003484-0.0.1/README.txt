This is a package for TOPSIS created by me. References are given in the code if want to understand it
Run the program through command line as:
Usages: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>
Example: python 101556.py 101556-data.csv “1,1,1,2” “+,+,-,+” 101556-result.csv
Program contains the following checkers:
• Correct number of parameters (inputFileName, Weights, Impacts, resultFileName).
• Show the appropriate message for wrong inputs.
• Handling of “File not Found” exception
• Input file must contain three or more columns.
• From 2nd to last columns must contain numeric values only (Handling of non-numeric values)
• Number of weights, number of impacts and number of columns (from 2nd to last columns) must
be same.
• Impacts must be either +ve or -ve.
• Impacts and weights must be separated by ‘,’ (comma).