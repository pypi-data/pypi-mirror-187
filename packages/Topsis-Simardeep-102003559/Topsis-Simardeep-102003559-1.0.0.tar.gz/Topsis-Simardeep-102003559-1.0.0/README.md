Topsis-Simardeep-102003559 is a Python library for dealing Multiple Criteria Decision Making(MCDM)
## Installation

```bash
pip install Topsis-Simardeep-102003559
```

## Usage

Enter csv filename followed by _.csv_ extentsion, then enter the _weights_ string with values separated by commas, followed by the _impacts_ string with comma separated signs _(+,-)_ and name of file followed by -.csv- extension in which the user wants the output file
```bash
topsis sample.csv "1,1,1,1" "-,+,+,+" sample_result.csv
```

## Example

#### sample.csv

A csv file showing data for different mobile handsets having varying features.

```

 Mobile Name  Cost  Storage Space  Camera  Looks 
0          M1   250             16      12      5     
1          M2   200             16       8      3     
2          M3   300             32      16      4     
3          M4   275             32       8      4     
4          M5   225             16      16      2     

``` 

weights string =  "0.25,0.25,0.25,0.25"

impacts string =  "-,+,+,+"

### input:

```python
topsis sample.csv "0.25,0.25,0.25,0.25" "-,+,+,+" sample_result.csv
```

### output:
```

 Mobile Name  Cost  Storage Space  Camera  Looks  Performance  Rank
0          M1   250             16      12      5     0.534277     3
1          M2   200             16       8      3     0.308368     5
2          M3   300             32      16      4     0.691632     1
3          M4   275             32       8      4     0.534737     2
4          M5   225             16      16      2     0.401046     4

An output csv file will also be auto generated.
``` 

## License
2023 Simardeep Singh

This repository is licensed under the MIT license. See LICENSE for details.
