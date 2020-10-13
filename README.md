# 5391-shtuff
Assignments and Uploads for Scientific programming PHYS 5391-001

There is a separate folder for each homework assignment. Homework notes are provided for each homework below.

-------------------------------------------------------------------------------------

Homework 1 NOTES:

To get a correct pdf rendition of the homework assignment, run the following commands:

$ pdflatex filename.tex

$ bibtex filename

$ pdflatex filename.tex

$ pdflatex filename.tex

(run pdflatex twice to ensure crossreferencing is correct)

ALTERNATE COMPILING METHOD - ensures no warnings are generated with the use of the tikZ-Feynman package:

$ lualatex filename.tex

$ bibtex filename

$ lualatex filename.tex

$ lualatex filename.tex

-------------------------------------------------------------------------------------

Homework 2 NOTES:

Package dependencies:

numpy
datetime
re
pandas
matplotlib
sciprog (file found on canvas)

all of these must be in the python path for the code to work

to produce my code for questions 1-2, run the following code:
$ python hw2_prob1-2.py

to produce my code for question 3, run the following code:
$ python hw2_prob3.py


-------------------------------------------------------------------------------------

Homework 3 NOTES:

Package dependencies:

matplotlib
sciprog (file found on canvas)
datetime
os
read_dst

IMPORTANT: read_dst is included in the git repo, you must put this file in your python path for the code to run correctly.

to reproduce the plots from my LaTeX file, run the following code from the hw3 directory:

$ python hw3.py
