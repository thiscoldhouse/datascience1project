rm -f output/papers.db
alembic upgrade head
python create_database.py 
