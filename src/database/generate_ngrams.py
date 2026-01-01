import pandas as pd
from models import SessionFactory, Paper
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
stop = [
    'elsevier', 'rights', 'reserved', 'mesh', 'taylor', 'francis', 'copyright', 'llc', 'bt', 'lftb', 'springer', 'ieee',
]

session = SessionFactory()
tokens = word_tokenize(
    ' '.join([
        '. '.join((paper.title, paper.abstract))
        for paper in session.query(Paper).all()
    ])
)
tokens = [
    t.lower() for t in tokens    
    if t.isalpha() and not
    any([w in t.lower() for w in stop])
]

bigrams = Counter()
trigrams = Counter()
fourgrams = Counter()
fivegrams = Counter()
sixgrams = Counter()

bigrams.update(ngrams(tokens, 2))
trigrams.update(ngrams(tokens, 3))
fourgrams.update(ngrams(tokens, 4))
fivegrams.update(ngrams(tokens, 5))
sixgrams.update(ngrams(tokens, 6))

print(pd.DataFrame({
    '2': [' '.join(b[0]) for b in bigrams.most_common(50)],
    '3': [' '.join(b[0]) for b in trigrams.most_common(50)],
    '4': [' '.join(b[0]) for b in fourgrams.most_common(50)],
    '5': [' '.join(b[0]) for b in fivegrams.most_common(50)],
    '6': [' '.join(b[0]) for b in sixgrams.most_common(50)],
}).to_markdown())

pd.DataFrame({
    '2': [' '.join(b[0]) for b in bigrams.most_common(250)],
    '3': [' '.join(b[0]) for b in trigrams.most_common(250)],
    '4': [' '.join(b[0]) for b in fourgrams.most_common(250)],
    '5': [' '.join(b[0]) for b in fivegrams.most_common(250)],
    '6': [' '.join(b[0]) for b in sixgrams.most_common(250)],
}).to_csv('ngrams.csv')




