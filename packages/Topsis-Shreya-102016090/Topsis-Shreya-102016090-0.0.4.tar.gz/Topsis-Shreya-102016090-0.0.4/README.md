# Topsis-Shreya-102016090

**Assignment-1 (UCS654)**
_Submitted By: **Shreya Saxena**_
_Roll no: **102016090**_
_Group: **3CS12**_

## What is TOPSIS?

**T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal **S**olution
It is used as a multi-criteria decision making method.

<br>

Topsis-Shreya-102016090 is a Python library for dealing with Multiple Criteria Decision Making(MCDM) problems by using Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Topsis-Shreya-102016090.

```
>> pip install Topsis-Shreya-102016090
```

## Usage

python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>

```
>> python 101556.py 101556-data.csv “1,1,1,2” “+,+,-,+” 101556-result.csv
```

## Example

#### data.csv

The decision matrix should be constructed with each row representing a Model alternative, and each column representing a criterion like Accuracy, R<sup>2</sup>, Root Mean Squared Error, Correlation, and many more.

| Model | Correlation | R<sup>2</sup> | RMSE | Accuracy |
| ----- | ----------- | ------------- | ---- | -------- |
| M1    | 0.79        | 0.62          | 1.25 | 60.89    |
| M2    | 0.66        | 0.44          | 2.89 | 63.07    |
| M3    | 0.56        | 0.31          | 1.57 | 62.87    |
| M4    | 0.82        | 0.67          | 2.68 | 70.19    |
| M5    | 0.75        | 0.56          | 1.3  | 80.39    |

Weights (`weights`) is not already normalised will be normalised later in the code.

Information of benefit positive(+) or negative(-) impact criteria should be provided in `impacts`.

### Input:

```python
topsis data.csv "0.25,0.25,0.25,0.25" "+,+,-,+" result.csv
```

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

## Other notes

- The first column and first row are removed by the library before processing, in attempt to remove indices and headers. So make sure the csv follows the format as shown in data.csv.
- Make sure the csv does not contain categorical values

## License

[MIT](https://choosealicense.com/licenses/mit/)
