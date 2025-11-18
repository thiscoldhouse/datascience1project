set -e

mkdir -p output
mkdir -p ../networks/input

rm -f output/papers.db
alembic upgrade head
python create_database.py

cd ../networks/input
rm -f papers.db
ln -s ../../database/output/papers.db papers.db
cd -
