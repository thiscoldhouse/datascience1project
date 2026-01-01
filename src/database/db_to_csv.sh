#!/bin/bash

set -e

sqlite3 output/papers.db << eom
.headers on
.mode csv
.output output/paper.csv
SELECT * from paper;
.quit
eom

sqlite3 output/papers.db << eom
.headers on
.mode csv
.output output/author.csv
SELECT * from author;
.quit
eom

sqlite3 output/papers.db << eom
.headers on
.mode csv
.output output/keyword.csv
SELECT * from keyword;
.quit
eom

sqlite3 output/papers.db << eom
.headers on
.mode csv
.output output/citation.csv
SELECT * from keyword;
.quit
eom

