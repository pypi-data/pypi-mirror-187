# Topsis implemented by Harsh Paba

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   

## Functionality of the package

- Outputs the performance score and rank corresponding to each row of the dataset.

## Usage

- Make sure you have Python installed in your system.
- Run the following command in terminal.
 ```
  pip install topsis-harsh-102003675
  ```
## Example
  ```
  from topsis_harsh_102003675 import main
  inputFile=sys.argv[1]
  weight=sys.argv[2]
  impact=sys.argv[3]
  outputFile=sys.argv[4]
  main.find_rank(inputFile,weight,impact,outputFile)
  ```

## Run the following Script.
 ```
 python test.py <inputFile.csv> weights impacts <outputFile.csv>
 ```

# Note
- Rank 1 corresponds to minimum performance score and so on.


