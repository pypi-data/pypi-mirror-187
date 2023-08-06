## Topsis_Vikas

# TOPSIS

Submitted By: **Vikas Singh - 102067010**.

Type: **Package**.

Title: **TOPSIS method for multiple-criteria decision making (MCDM)**.

Author: **Vikas Singh**.

Maintainer: **Vikas Singh <vs8422135@gmail.com>**.

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
>> pip install TOPSIS-Vikas-102067010
```

### In Command Prompt

```
>> topsis 102067010-data.csv "1,1,1,1" "+,+,-,+" 102067010-result.csv
```

## Input file (data.csv)

The decision matrix should be constructed with each row representing a Model alternative, and each column representing a criterion like Accuracy, R<sup>2</sup>, Root Mean Squared Error, Correlation, and many more.

| Mobile Name  | Price($) | Storage(GB) | Camera(MP) | Looks |
| Moto g82     | 250      | 16          | 12         | 5     | 
| Samsung S32  | 200      | 16          | 8          | 3     |
| Oppo F17     | 300      | 32          | 16         | 4     | 
| Iphone 14    | 275      | 32          | 8          | 4     | 
| Redmi Note12 | 225      | 16          | 16         | 2     |
Weights (`weights`) is not already normalised will be normalised later in the code.

Information of benefit positive(+) or negative(-) impact criteria should be provided in `impacts`.

<br>

## Output file (result.csv)
| Mobile Name  | Price($) | Storage(GB) | Camera(MP) | Looks | Topsis Score | Rank |
| Moto g82     | 250      | 16          | 12         | 5     | 0.5682       | 3    |
| Samsung S32  | 200      | 16          | 8          | 3     | 0.1658       | 5    |
| Oppo F17     | 300      | 32          | 16         | 4     | 0.8342       | 1    |
| Iphone 14    | 275      | 32          | 8          | 4     | 0.5691       | 2    |
| Redmi Note12 | 225      | 16          | 16         | 2     | 0.3096       | 4    |

<br>
The output file contains columns of input file along with two additional columns having **Topsis_score** and **Rank**