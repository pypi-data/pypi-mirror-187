# Topsis Python Package

This is a Python Package implementing Topsis Multi-Criteria Decison Making method.<br />
It is a simple implementation using
    - pandas
    - numpy<br />
It stores the output as a csv file with user-specified name.<br/>
Output contains the original data with two additional columns i.e. Topsis Score and Rank based on the score.

## Installation

To install the package<br />

```pip install topsis-kanuj-102017188```

## Usage

To use the package from the command line (Data file and result file name should contain .csv extension)<br />

```topsis [data file name] [weights as string seperated by ','] [impacts as string seperated by ','] [result data file name]```

For example<br />

```topsis data.csv "1,1,1,1,1" "+,+,+,-,+" result.csv```

## Sample

Data Sample<br />

```
Model,StorageSpace,Camera,Price,Looks
M1,16,12,250,5
M2,16,8,200,3
M3,32,16,300,4
M4,32,8,275,4
M5,16,16,225,2
```
Sample topsis command<br />

```topsis data.csv "0.25,0.25,0.25,0.25" "+,+,-,+" result.csv```

Sample Output file<br />
```
Model,StorageSpace,Camera,Price,Looks,TopsisScore,Rank
M1,16,12,250,5,0.534277,3.0
M2,16,8,200,3,0.308368,5.0
M3,32,16,300,4,0.691632,1.0
M4,32,8,275,4,0.534737,2.0
M5,16,16,225,2,0.401046,4.0
```

## Notes

The data should only contain numerical data.<br />