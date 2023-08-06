Ekaspreet-topsis-102017078


# Topsis in Python  
Author: **Ekaspreet 102017078**  
Maintainer: **Ekaspreet <ekaspreet0209@gmail.com>**.

TOPSIS: It is a for Multiple Criteria Decision Making,A Technique for Order Preference by Similarity to Ideal   
More details at [wikipedia](https://en.wikipedia.org/wiki/TOPSIS).  
<br>
<br>


### In Command Prompt

```
>> topsis data.csv "1,1,1,1" "+,+,-,+" result.csv
```

## Input file (data.csv)
| Model | Correlation | R<sup>2</sup> | RMSE | Accuracy | 
| ----- | ----------- | ------------- | ---- | -------- |
| M1    | 0.79        | 0.62          | 1.25 | 60.89    |
| M2    | 0.66        | 0.44          | 2.89 | 63.07    |
| M3    | 0.56        | 0.31          | 1.57 | 62.87    |
| M4    | 0.82        | 0.67          | 2.68 | 70.19    |
| M5    | 0.75        | 0.56          | 1.3  | 80.39    |

Weights (`weights`) is not already normalised will be normalised later in the code.

Information of positive(+) or negative(-) impact criteria should be provided in `impacts`.

<br>

## Output file (result.csv)

| Model | Correlation | R<sup>2</sup> | RMSE | Accuracy | Score  | Rank |
| ----- | ----------- | ------------- | ---- | -------- | ------ | ---- |
| M1    | 0.79        | 0.62          | 1.25 | 60.89    | 0.7722 | 2    |
| M2    | 0.66        | 0.44          | 2.89 | 63.07    | 0.2255 | 5    |
| M3    | 0.56        | 0.31          | 1.57 | 62.87    | 0.4388 | 4    |
| M4    | 0.82        | 0.67          | 2.68 | 70.19    | 0.5238 | 3    |
| M5    | 0.75        | 0.56          | 1.3  | 80.39    | 0.8113 | 1    |

<br>
The output file contains columns of input file along with two additional columns having **Score** and **Rank**
