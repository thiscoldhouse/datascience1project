To build this project from scratch and run all the analysis (with the exception of `/predict`, run `./run.sh`.

*Warning: This is intended to be run only once. It will overwrite anything that you have already done*

# Code

## Organization

- `/data` - contains raw data
- `/database` - creates the sqlite database that the rest of the project uses
- Analysis folders: `/citations`, `/networks`, `/term_frequency`, and `/prediction`
- Work in Progres folders: `/metaphorometer`, `/misc`. 
  
## Workflows

Work that has nowhere to live yet should go in `/misc`, then spin into its own folder (like `metaphorometer` has done). 

With the exception of `/prediction`, all important code folders are organized so that there are four kinds of files:

- `./input/`
- `./output/`
- `./config.py`
- Various python files

`config.py` is where manual settings should go, like parameter, colors, etc. 

Python files should only read from their `/input` folder. The `/database/build_database.sh` script will automatically populate those with a symlink from the database (or, in the case of `term_frequency`, with a CSV version, which it uses for historical reasons, since that process predates our database).

Python files should only output to `/output`. If another process needs that data, that data creation should also create a symlink.
