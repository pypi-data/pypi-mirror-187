# Topsis
The package includes a TOPSIS class that can be used to perform the analysis. The class takes the following parameters:

Source File: Contains a decision matrix with rows as alternatives and columns as criteria
Weights: A string representing the weight of each criterion
Impacts: A string representing the impact of each criterion (+ for positive impact, - for negative impact)

# Algorithm :    
### STEP 1 :    
Create an evaluation matrix consisting of m alternatives and n criteria, with the intersection of each alternative and criteria.   
Apply any preprocessing if required.   
### STEP 2 :   
The matrix is then normalised using the norm.

### STEP 3 :
Calculate the weighted normalised decision matrix.

### STEP 4 :
Determine the worst alternative and the best alternative.

### STEP 5 :
Calculate the L2-distance between the target alternative i and the worst condition.

### STEP 6 :
Calculate the similarity to the worst condition.

### STEP 7 :
Rank the alternatives according to final performance scores.   

## To install this package :
Use pip install VanshikaPackage
`pip install VanshikaPackage`

## To run the topsis function 
`topis <sourcefile.csv> "<weights_seperated_by_commas>" "<impact_seperated_by_commas>" <destinationfilename.csv>`
## example 
`topsis srcfile.csv "1,1,1,2" "+,+,+,-" dstfile.csv`
## License

© 2023 Vanshika

This repository is licensed under the MIT license. See LICENSE for details.
