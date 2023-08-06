# Project Description
## Topsis

TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) is a Multi-Criteria Decision Ananlysis (MCDA) method that is used to solve multiple criteria decision making problems.

It uses the fundamental premise that the best solution has the shortest distance from the positive-ideal solution, and the longest distance from the negative-ideal one and ranks solutions that have multiple criterias.

## Installation
Use ```pip``` to install:
```
pip install topsis-ananya-102017024
```
**Prerequisite**
Libraries needed to be downloaded before running this package are :
- Numpy
- Pandas

## Usage
Run ```topsis``` in the input file's directory as follows:
```
topsis <input_file_name> <weights> <impacts> <output_file_name>
```
For example,
Use quotation marks while including spaces in any argument:
```
topsis data.csv "1, 1, 1, 1" "+, -, +, -" result.csv
```
or vectors can be entered without any space
```
topsis data.csv 1,1,1,1 +,-,+,- result.csv
```

##### Note that
- Input file must contain three or more columns.
- Except the first column of the input file the rest must be numeric
- Weights must be numeric
- Impacts must be either 
  - ```+``` (for features that are to be maximised) 
  - ```-``` (for features that are to be minimized)
- Both Impacts & Weights must be seperated by a comma ```,``` 

## Example
**input.csv**
| Attribute | Price | Storage | Camera | Looks|
| ------ | ------ | ------ | ------ | ------ |
| M1 | 250 | 16 | 12 | 5 |
| M2 | 200 | 16 | 8 | 3 |
| M3 | 300 | 32 | 16 | 4 |
| M4 | 275 | 32 | 8 | 4 |
| M5 | 225 | 16 | 16 | 2 |

On running 
``` 
topsis input.csv "0.25,0.25,0.25,0.25" "-,+,+,+" output.csv
```

**output.csv**
| Attribute | Price | Storage | Camera | Looks| Topsis Score | Rank |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| M1 | 250 | 16 | 12 | 5 | 0.534269 | 3 |
| M2 | 200 | 16 | 8 | 3 | 0.308314 | 5 |
| M3 | 300 | 32 | 16 | 4 | 0.691686 | 1 |
| M4 | 275 | 32 | 8 | 4 | 0.534807 | 2 |
| M5 | 225 | 16 | 16 | 2 | 0.401222 | 4 |


## License

MIT
