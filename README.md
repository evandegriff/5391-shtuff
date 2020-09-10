# 5391-shtuff
Assignments and Uploads for Scientific programming PHYS 5391-001

to get a correct pdf file for the homework assignment, run the following commands:

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