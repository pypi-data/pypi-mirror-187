# Deepak-102003483

## What is TOPSIS
Topsis stands for <b>T</b>echnique for <b>O</b>rder <b>P</b>reference by <b>S</b>imilarity to <b>I</b>deal <b>S</b>olution (TOPSIS).  Topsis was originated back in the 1980s and was used for making decisions which are subjected to multiple-criteria.
<br> 
TOPSIS takes in the use of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.

## Package Installation 
```pip install Deepak-102003483==1.1.10```

## Input File in CSV Format
Input file must contain <b>Three or more columns</b>
<br>
First column contains the <b>Object Name / Variable Name </b>
<br>
Rest of the other columns contains only numeric values

## Usage Method

Command Prompt<br>
```
python <python_file> <Input_Data_File> <Weights> <Impacts> <Result_File_Name>
```
<br>

<br>
python_file -> Python Code file for Topsis Calculation <br>
Input_Data_File -> CSV file name <br>
Weights -> Weights for each Column <br>
Impacts -> Maximaization('+'), Minimization('-')  <br>
Result_File_Name -> CSV file name to store result <br>


Example:<br>
```
python 102003483.py 102003483-data.csv “1,1,1,1,1” “+,-,+,-,+” 102003483-result-1.csv
python 102003483.py 102003483-data.csv “2,2,3,3,4” “-,+,-,+,-” 102003483-result-2.csv
```
<br><br>
<i>Note: The Weights and Impacts should be comma (',') seperated and Input CSV file should be in pwd(Present Working Directory).</i> 

## Functions and Return Values

```
function = topsis_102003483()
return values = Creates a CSV file with the Topsis Rank and Performance Score
```

## Sample input data
| Fund Name       | P1 | P2 | P3 | P4 | P5 |
| ------------- |:-------------:| -----:|-----:|-----:|-----:|
| M1    | 0.62 | 0.38 | 3.8 | 33.8 | 9.65  | 
 | M2    | 0.75 | 0.56 | 5.7 | 50.3 | 14.33 | 
 | M3    | 0.95 | 0.90 | 6.5 | 65.6 | 18.49 | 
 | M4    | 0.61 | 0.37 | 6.2 | 43.6 | 12.70 | 
 | M5    | 0.60 | 0.36 | 6.4 | 61.2 | 17.14 | 
 | M6    | 0.76 | 0.58 | 5.3 | 68.0 | 18.66 | 
 | M7    | 0.66 | 0.44 | 6.2 | 47.2 | 13.63 | 
 | M8    | 0.80 | 0.64 | 5.7 | 37.1 | 11.06 | 


## Sample output data
| Fund Name       | P1 | P2 | P3 | P4 | P5 | Topsis Score | Rank |
| ------------- |:-------------:| -----:|-----:|-----:|-----:| ---: | ---: |
| M1    | 0.62 | 0.38 | 3.8 | 33.8 | 9.65  |  0.317272185       | 8           | 
| M2    | 0.75 | 0.56 | 5.7 | 50.3 | 14.33 |  0.452068871       | 4           | 
| M3    | 0.95 | 0.90 | 6.5 | 65.6 | 18.49 |  0.689037307       | 1           | 
| M4    | 0.61 | 0.37 | 6.2 | 43.6 | 12.70 |  0.340383903       | 7           | 
| M5    | 0.60 | 0.36 | 6.4 | 61.2 | 17.14 |  0.367206376       | 6           |
| M6    | 0.76 | 0.58 | 5.3 | 68.0 | 18.66 |  0.481350901       | 3           | 
| M7    | 0.66 | 0.44 | 6.2 | 47.2 | 13.63 |  0.372999972       | 5           | 
| M8    | 0.80 | 0.64 | 5.7 | 37.1 | 11.06 |  0.51226635        | 2           | 