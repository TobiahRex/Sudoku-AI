# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: By definition, constraint propagation is the process of finding a solution to a set of constraints that impose conditions that variables must satisfy. 
In the naked twins problem, we impose the constraint that each cell in the intersection of the twins peer groups' must not contain the two values given by the twin pair. 
In particular, this constraint is effectively propagated through the peer group intersection for each naked twin. 
The process of modifying the peer group intersection based on constraints imposed by the twin group is by definition constraint propagation. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We should iteratively apply eliminate and only_choice with the added constraint that the numbers 1-9 must appear exactly once in each diagonal unit on the board. 
With this added constraint, the peer group of each cell will be all boxes that belong to either the same row, column, 3 by 3 square or diagonal unit (if one exists). 
In particular, each cell on each diagonal unit will have an augmented peer group containing cells which belong to the same diagonal unit. 
Constraint propagation is used on each iteration of the function calls (eliminate and only_choice) since we use constraints to solve or eliminate certain possibilities for each cell in the peer group and/or unit. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system. - 

