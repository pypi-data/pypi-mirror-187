## Topsis_Akshat

# TOPSIS

Submitted By: **Akshat Girdhar - 102017147**.

Title: **TOPSIS method for Multiple Criteria Decision Making (MCDM)**.

Version: **1.0.4**.

Author: **Akshat Girdhar**.

Maintainer: **akshatgirdhar02@gmail.com**.

Description: **Evaluation of alternatives based on multiple criteria using TOPSIS method.**.

---

## What is TOPSIS?

Technique for Order Preference by Similarity to Ideal Solution
(TOPSIS) is a multi-criteria decision making method.
TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution,
and greatest distance from the negative-ideal solution.
<br>
<strong>Weight</strong> vector represent the importance we want to give to a particular feature.
<br>
<strong>Impacts</strong> tells whether we want to maximize or minimize that feature. <strong>'+'</strong>->For maximizing,<strong>'-'</strong>->For minimizing

<br>

## How to install this package:

```
pip install Topsis-Akshat-102017147
```

### Usage

```
topsis <InputDataFile.csv> <Weights> <Impacts> <Result.csv>
```

weights and impacts can be given in string format each separated by comma(',') like-:

```
topsis data.csv "1,1,1,1" "+,-,+,-" result.csv
```
or can also be given without double quotes("") like-:
```
topsis data.csv 1,1,1,1 +,-,+,- result.csv
``` 
But,each argument should be separated by a space.

# Example
Let's understand how to use the package with the help of an example.

## Input file (data.csv)

| Model | Price (in $)| Storage Space (in GB) |Camera (in MP)| Looks    |
| ----- | ----------- | ----------------------| -------------| -------- |
| M1    | 250         | 16                    | 12           | 5        |
| M2    | 200         | 16                    | 8            | 3        |
| M3    | 300         | 32                    | 16           | 4        |
| M4    | 275         | 32                    | 8            | 4        |
| M5    | 225         | 16                    | 16           | 2        |

weights =[1,1,1,1]
<br>
impacts=["-,+,+,+"]

### Input
```
topsis data.csv "1,1,1,1" "-,+,+,+" result.csv
```

<br>

## Output file(result.csv)

| Model | Price (in $)| Storage Space (in GB) |Camera (in MP)| Looks    |Topsis Score|Rank|
| ----- | ----------- | ----------------------| -------------| -------- |------------|----|  
| M1    | 250         | 16                    | 12           | 5        | 0.5343     |3   |
| M2    | 200         | 16                    | 8            | 3        | 0.3085     |5   |
| M3    | 300         | 32                    | 16           | 4        | 0.6916     |1   |
| M4    | 275         | 32                    | 8            | 4        | 0.5348     |2   |
| M5    | 225         | 16                    | 16           | 2        | 0.4010     |4   |

<br>
The output file contains columns of input file along with two additional columns having <strong>Topsis Score</strong> and <strong>Rank</strong>