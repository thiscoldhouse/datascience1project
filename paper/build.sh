#!/bin/bash
set -e

rm -f main.aux main.bbl main.blg main.run.xml main.toc main.lof main.lot main.out main.log

pdflatex main
bibtex main
pdflatex main
pdflatex main

rm -f main.aux main.bbl main.blg main.run.xml main.toc main.lof main.lot main.out

