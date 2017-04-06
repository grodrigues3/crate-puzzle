# crate-puzzle
Kung Fu Create Puzzle Solver
Game: http://www.puzzlebeast.com/crate/

Author: Garrett Rodrigues
Date: April 2014

# Dependencies:
	1)Python 2.7 (probably backwards compatible with anything 2.xx)
	2)Numpy 
		To install on Ubuntu:
			sudo apt-get install python-numpy
		Other:
			http://docs.scipy.org/doc/numpy/user/install.html
	3)simplejson:
		To install:
			https://pypi.python.org/pypi/simplejson/


# Instructions for Running the Code

1- The code relies on the current directory structure. 
	/src
		/sample_games
	/answers
		/board1_solution.json
		...
		/boardn_solution.json

1- Then, once numpy is installed, run the program by typing
	$ python final_kung_fu.py
	
1- Answers should be written to the answers directory in the correct json format
