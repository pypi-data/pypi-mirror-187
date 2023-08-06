# Topsis implemented by Anupam Katoch

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   

## Functionality of the package

- Outputs the performance score and rank corresponding to each row of the dataset.

## Usage

- Make sure you have Python installed in your system.
- Run the following command in terminal.
 
  pip install topsis_Anupam_102003692
  
## Example
  
  from topsis_Anupam_102003692 import main
  ip=sys.argv[1]
  wt=sys.argv[2]
  im=sys.argv[3]
  op=sys.argv[4]
  main.find_rank(ip,wt,im,op)
  

## Run the following Script.
 ```
  python test.py <inputFile.csv> weights impacts <outputFile.csv>