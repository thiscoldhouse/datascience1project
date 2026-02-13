#!/bin/bash
set -e

rm -rf citations-img misc-img network-img term_frequency-img

cp -r ../src/citations/output citations-img/
cp -r ../src/misc/output misc-img/
cp -r ../src/networks/output network-img/
cp -r ../src/term_frequency/output term_frequency-img/

rm -f main.aux main.bbl main.blg main.run.xml main.toc main.lof main.lot main.out main.log

pdflatex main
bibtex main
pdflatex main
pdflatex main

rm -f main.aux main.bbl main.blg main.run.xml main.toc main.lof main.lot main.out

