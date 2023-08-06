# TOPSIS

Title: **TOPSIS method for multiple-criteria decision making (MCDM)**.

Version: **1.0.7**.

Author: **Arhanjit Sodhi**.

Description: **Evaluation of alternatives based on multiple criteria using TOPSIS method.**

---

## How to install this package:

```
>> pip install Topsis-Arhanjit-102003116
```

### In Command Prompt

```
>> topsis inputdata.csv "1,1,1,1,1" "+,+,-,+,-" resultdata.csv
```

## Input file (data.csv)

| Model | Correlation | R^2  | RMSE | Accuracy |
| ----- | ----------- | ---- | ---- | -------- |
| P1    | 0.79        | 0.62 | 1.25 | 60.89    |
| P2    | 0.66        | 0.44 | 2.89 | 63.07    |
| P3    | 0.56        | 0.31 | 1.57 | 62.87    |
| P4    | 0.82        | 0.67 | 2.68 | 70.19    |
| P5    | 0.75        | 0.56 | 1.3  | 80.39    |

<br>

## Output file (result.csv)

| Model | Correlation | R^2  | RMSE | Accuracy | Topsis_score | Rank |
| ----- | ----------- | ---- | ---- | -------- | ------------ | ---- |
| P1    | 0.79        | 0.62 | 1.25 | 60.89    | 0.7722       | 2    |
| P2    | 0.66        | 0.44 | 2.89 | 63.07    | 0.2255       | 5    |
| P3    | 0.56        | 0.31 | 1.57 | 62.87    | 0.4388       | 4    |
| P4    | 0.82        | 0.67 | 2.68 | 70.19    | 0.5238       | 3    |
| P5    | 0.75        | 0.56 | 1.3  | 80.39    | 0.8113       | 1    |

<br>

The output file contains columns of input file along with two additional columns having Topsis_score and Rank
