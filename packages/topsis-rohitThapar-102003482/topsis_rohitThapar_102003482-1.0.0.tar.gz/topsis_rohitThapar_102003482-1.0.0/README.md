# TOPSIS

Title: **TOPSIS method for multiple-criteria decision making (MCDM)**.

Version: **1.0.0**.

Author: **Rohit Thapar**.

Description: **Evaluation of alternatives based on multiple criteria using TOPSIS method.**

---

## How to install this package:

```
>> pip install topsis-rohitThapar-102003482
```

### In Command Prompt

```
>> topsis data.csv "1,1,1,1,1" "+,+,-,+,-" output.csv
```

## Input file (data.csv)

    Fund Name          P1        P2        P3        P4        P5    
--  -----------  --------  --------  --------  --------  --------  
 0  M1           0.395818  0.419886  0.221712  0.485574  0.467084      
 1  M2           0.271291  0.196656  0.221712  0.485574  0.4624        
 2  M3           0.413607  0.457091  0.286079  0.45586   0.446787       
 3  M4           0.302422  0.244491  0.479183  0.28917   0.310695       
 4  M5           0.271291  0.196656  0.479183  0.226118  0.252928      
 5  M6           0.413607  0.457091  0.221712  0.226118  0.234713      
 6  M7           0.413607  0.457091  0.286079  0.28917   0.297164      
 7  M8           0.302422  0.244491  0.479183  0.226118  0.253969      

<br>

## Output file (result.csv)
    Fund Name          P1        P2        P3        P4        P5    Topsis Score    Rank
--  -----------  --------  --------  --------  --------  --------  --------------  ------
 0  M1           0.395818  0.419886  0.221712  0.485574  0.467084       0.924217        1
 1  M2           0.271291  0.196656  0.221712  0.485574  0.4624         0.591977        3
 2  M3           0.413607  0.457091  0.286079  0.45586   0.446787       0.864965        2
 3  M4           0.302422  0.244491  0.479183  0.28917   0.310695       0.208741        6
 4  M5           0.271291  0.196656  0.479183  0.226118  0.252928       0.0340168       8
 5  M6           0.413607  0.457091  0.221712  0.226118  0.234713       0.530087        5
 6  M7           0.413607  0.457091  0.286079  0.28917   0.297164       0.577036        4
 7  M8           0.302422  0.244491  0.479183  0.226118  0.253969       0.110191        7

<br>

The output file contains columns of input file along with two additional columns having Topsis_score and Rank