set -e

mkdir -p output
mkdir -p ../networks/input
mkdir -p ../citations/input
mkdir -p ../1432/input

rm -f output/papers.db
alembic upgrade head
python create_database.py

cd ../networks/input
rm -f papers.db
ln -s ../../database/output/papers.db papers.db
cd -

cd ../citations/input
rm -f papers.db
ln -s ../../database/output/papers.db papers.db
cd -

cd ../1432_allotax/input
rm -f papers.db
ln -s ../../database/output/papers.db papers.db
cd -
