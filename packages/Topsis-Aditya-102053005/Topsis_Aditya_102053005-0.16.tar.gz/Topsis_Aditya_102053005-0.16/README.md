# Topsis Package by Aditya Kalhan
Roll Number : 102053005 <br>
Subgroup : 3COE18 <br>
It takes a csv file, weights (seperated by comma) , impacts (+ or -) and outputs a result file.
# What is Topsis
TOPSIS is based on the fundamental premise that the best solution has the shortest distance from the positive-ideal solution, and the longest distance from the negative-ideal one.<br>
Selecting an appropriate Multiple Attribute Decision Making (MADM) method for a given MADM problem is always a challenging task.<br>
Within the MADM domain, the Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is highly regarded, applied and adopted MADM method due to its simplicity and underlying concept that the best solution is the one closest to the positive ideal solution and furthest from the negative ideal solution.<br>


## Installation
Use pip installer <br>
``` pip install Topsis-Aditya-102053005 == 0.16 ```

## How to use it
Open terminal and type <br>
``` 102053005 sample.csv "1,1,1,1" "+,+,-,+" result.csv ```

## Example 
| Model | Storage Space | Camera | Price | Looks |  
|-----------|:-----------:|-----------:|-----------:|-----------:|
| M1 | 16 | 12 | 250 | 5 |  
| M2 | 16 | 8 | 200 | 3 |  
| M3 | 32 | 16 | 300 | 4 |  
| M4 | 32 | 8 | 275 | 4 |  
| M5 | 16 | 16 | 225 | 2 |  

weights = [1,1,1,1] <br>
impact = ["+","+","-","+"]


## Output
| Model | Storage Space | Camera | Price | Looks | Topsis Score | Rank |
|-----------|:-----------:|-----------:|-----------:|-----------:|-----------:|-----------:|
| M1 | 16 | 12 | 250 | 5 |  0.534269 | 3 |~
| M2 | 16 | 8 | 200 | 3 |  0.308314 | 5 |
| M3 | 32 | 16 | 300 | 4 |  0.691686 | 1 |
| M4 | 32 | 8 | 275 | 4 |  0.534807 | 2 |
| M5 | 16 | 16 | 225 | 2 |  0.401222 | 4 |

Output will be saved in a CSV file whose name will be provided in the command line.
It will have all the columns along with the Topsis Score and Ranks.<br><br>





