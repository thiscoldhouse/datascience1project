#!/bin/bash

set -e

echo "This script builds the database from scratch and installs python requirements. It will delete any version of the databse that you currently have. Make sure that you are in the right python environment before you continue."
read -p "Are you sure you want to continue? [y/N] " -n 1 -r
echo "" 
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi


echo "Installing requirements"
#pip install -r requirements.txt

cd database
echo "Building the database. This might take awhile..."
#./build_database.sh
cd -

echo "Running community detection. This takes a little bit too."
python nentworks/network_detection.py --relabel 1

echo "Generating term frequency graph. This is quicker."
python term_frequency/proposal_figure.py

echo "Generating citations figures."
python citations/make_figures.py

echo "All that's left is the prediction. To do that, you'll have to run python notebooks manually in /prediction"

echo "Success. Exiting."
