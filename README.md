# CS-pattern-reduction

## Files
### CuttingStock
This is the main file that coordinates the overall KPB heuristic.
The bulk of the code here is in the CuttingStockProblem class, which is innitialised with the problem, and then run using a function of the class.
There is also a function that reads one of the test files provided, and automatically runs the pattern reduction heuristic.

### seed_class
This contains the class for the nodes of the tree which we traverse to run the heuristic. 

### ReturnSeeds
This file contains the knapsacking algorithm that we use to find seed patterns.

### BinPacking
This file contains the bin packing algorithm that we use to bin pack the non seed nodes.

### extract
This file contains the code used to read the test files.

### DynamicProgrammingAlgorithm
This file contains an algorithm that was developed early in the semester, which finds a solution to the cutting stock problem using a dynamic approach.
This code is not used in any other files, and functions as its own stand alone solver.

## Format
We store each strip as a dictionary with two keys, 'strip', which points to an array of sizes representing the construction of the strip itself, and 'amount', which holds the number of times this strip appears in the overall solution.
The dictionary is hashed with the string conversion of the strip, so if the strip were [1, 2, 3, 4, 5], then the dictionary key for that strip would be '[1, 2, 3, 4, 5]'.
