## Topsis_102003458

# TOPSIS

Submitted By: **Anshika Singla_102003458**.

Type: **Package**.

Title: **TOPSIS method for multiple-criteria decision making (MCDM)**.

Version: **0.2**.

Author: **Anshika Singla**.

Maintainer: **Anshika Singla <asingla2_be20@thapar.edu>**.

Description: **Evaluation of alternatives based on multiple criteria using TOPSIS method.**.

---

## What is TOPSIS?

**T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal **S**olution
(TOPSIS) originated in the 1980s as a multi-criteria decision making method.
TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution,
and greatest distance from the negative-ideal solution.

<br>

## How to install this package:

```
>> pip install Topsis_102003458_Anshika
```

### In Command Prompt

```
>> topsis 102003458-data.csv "1,1,1,1,1" "+,-,+,-,+" 102003458-result.csv
```

## Input file (data.csv)

| Fund Name | P1          | P2         |P3        | P4       | P5         |
| --------- | ----------- | ---------- | -------- | -------- | ---------- |
| M1        | 0.67        | 0.45       | 6.5      | 42.6     | 12.56      |
| M2        | 0.6         | 0.36       | 3.6      | 53.3     | 14.47      |
| M3        | 0.82        | 0.67       | 3.8      | 63.1     | 17.1       |
| M4        | 0.6         | 0.36       | 3.5      | 69.2     | 18.42      |
| M5        | 0.76        | 0.58       | 4.8      | 43       | 12.29      |
| M6        | 0.69        | 0.48       | 6.6      | 48.7     | 14.12      |
| M7        | 0.79        | 0.62       | 4.8      | 59.2     | 16.35      |
| M8        | 0.84        | 0.71       | 6.5      | 34.5     | 10.64      |

<br>

## Output file (result.csv)

| Fund Name | P1          | P2         |P3        | P4       | P5         | Topsis Score  | Rank  |
| --------- | ----------- | ---------- | -------- | -------- | ---------- | --------------|-------|
| M1        | 0.67        | 0.45       | 6.5      | 42.6     | 12.56      | 20.58         | 2     |
| M2        | 0.6         | 0.36       | 3.6      | 53.3     | 14.47      | 40.83         | 4     |
| M3        | 0.82        | 0.67       | 3.8      | 63.1     | 17.1       | 30.07         | 3     |
| M4        | 0.6         | 0.36       | 3.5      | 69.2     | 18.42      | 50.22         | 5     |
| M5        | 0.76        | 0.58       | 4.8      | 43       | 12.29      | 10.41         | 1     |
| M6        | 0.69        | 0.48       | 6.6      | 48.7     | 14.12      | 80.51         | 8     |
| M7        | 0.79        | 0.62       | 4.8      | 59.2     | 16.35      | 70.74         | 7     |
| M8        | 0.84        | 0.71       | 6.5      | 34.5     | 10.64      | 60.33         | 6     |

<br>

The output file contains columns of input file along with two additional columns having **Topsis_score** and **Rank**

