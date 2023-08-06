---
# TOPSIS
### Navreen Waraich
---
&nbsp;
###### This is a Python package curated to show topsis (Technique for Order of preference by similarity to Ideal Solution) ranking to measure the relative performance of each category by mathematical computation
&nbsp;
##### UCS633 Project Submission
*Name* - *Navreen Waraich* 
*Roll no.* - *102017150* 

The following are the pre-requisites:
	
* **Data**: The dataset of which topsis score is to be calculated.
* **Weights**: A List (int/float) of weights of all columns.
* **Impacts**: A List ('+'/'-') of all impacts of all columns. 
 
 ## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install Topsis-navreen-102017150
```
This will install the topsis package in your workspace.

##### The following exceptions are handled and should be taken care of:
* To check number of weights, impacts and number of columns to be same.
* To check contents of both weights and impacts list for any discrepancy.


Write the following in the editor to run the package
```sh
import Topsis-navreen-102017150
```
## Sample Input
Following is the input dataset.

|Fund Name|P1  |P2  |P3 |P4  |P5   |
|---------|----|----|---|----|-----|
|M1       |0.67|0.45|6.5|42.6|12.56|
|M2       |0.6 |0.36|3.6|53.3|14.47|
|M3       |0.82|0.67|3.8|63.1|17.1 |
|M4       |0.6 |0.36|3.5|69.2|18.42|
|M5       |0.76|0.58|4.8|43  |12.29|
|M6       |0.69|0.48|6.6|48.7|14.12|
|M7       |0.79|0.62|4.8|59.2|16.35|
|M8       |0.84|0.71|6.5|34.5|10.64|

```sh
weights = 1,1,1,1,1
impacts = '+','-','+','-','+'
``` 


```  

Output :  
|Fund Name|P1  |P2  |P3 |P4  |P5   |Topsis Score|Rank|
|---------|----|----|---|----|-----|------------|----|
|M1       |0.93|0.86|4.1|46.1|13   |0.368067725 |8   |
|M2       |0.67|0.45|6.1|44  |12.81|0.629815594 |1   |
|M3       |0.72|0.52|3.8|32.7|9.44 |0.488377092 |5   |
|M4       |0.73|0.53|4.1|45  |12.59|0.489923292 |4   |
|M5       |0.71|0.5 |3.4|55.5|15.03|0.461216998 |6   |
|M6       |0.74|0.55|7  |63.3|17.9 |0.603048108 |3   |
|M7       |0.95|0.9 |5.1|41.8|12.19|0.416449713 |7   |
|M8       |0.63|0.4 |7  |63.5|17.88|0.621465197 |2   |

