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
