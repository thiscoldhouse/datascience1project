# To run build_database

```
cd database
pip install -r requirements.txt
./build_database.sh
```

# To use DB as dataframe 

```
import sqlite3
import pandas as pd
cnx = sqlite3.connect('input/papers.db')

papers = pd.read_sql_query("SELECT * FROM paper", cnx)
authors =  pd.read_sql_query("SELECT * FROM author", cnx)
authors_to_papers =  pd.read_sql_query("SELECT * FROM paper_author", cnx)
keywords_to_papers = pd.read_sql_query("SELECT * FROM paper_keyword", cnx)
keywords =  pd.read_sql_query("SELECT * FROM keyword", cnx)
```
