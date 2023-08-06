# Topsis Python Package

This is a Python Package implementing Topsis Multi-Criteria Decison Making method.<br />
It is a simple implementation using
    - pandas
    - numpy<br />
It stores the output as a csv file with user-specified name.<br/>
Output contains the original data with two additional columns i.e. Topsis Score and Rank based on the score.

## Installation

To install the package<br />

```pip install topsis_17188```

## Usage

To use the package from the command line (Data file and result file name should contain .csv extension)<br />

```topsis [data file name] [weights as string seperated by ','] [impacts as string seperated by ','] [result data file name]```

For example<br />

```topsis data.csv "1,1,1,1,1" "+,+,+,-,+" result.csv```

## Notes
The data should only contain numerical data.<br />