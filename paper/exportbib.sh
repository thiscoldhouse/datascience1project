set -e

OUTFILE="allrefs.bib"

URL="http://127.0.0.1:23119/better-bibtex/export/library"

curl -sG "$URL" \
  --data-urlencode "format=bibtex" \
  --data-urlencode "exportNotes=false" \
  --data-urlencode "exportFileData=false" \
  -o "$OUTFILE"

echo "Zotero library exported to $OUTFILE"
