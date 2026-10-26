from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk import word_tokenize
import numpy as np
import os, sys

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../database'
    )
)
from models import Paper, Author, SessionFactory
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from config import stop

engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)

def main(community_col='community', target_communities=None, nterms=7):    
    if target_communities is None:
        target_communities = [
            5282,
            426,
            2350,
            1432,
            6075,
            1277,
        ]

    target_communities = list(set(target_communities))
    session = SessionFactory()
    texts = (
        session.query(
            getattr(Paper, community_col),
            functions.concat(
                Paper.title,
                ' ',
                Paper.abstract,
            )
        ).
        group_by(getattr(Paper, community_col))
    ).all()

    communities = [text[0] for text in texts]
    texts = [
        ' '.join(
            map(str, word_tokenize(text[1]))
        ).lower()
        for text in texts 
    ]

    results = []
    for ngram in (1,2):
        vectorizer = TfidfVectorizer(
            stop_words=stop,
            ngram_range=(ngram, ngram),
        )
        X = vectorizer.fit_transform(texts)
        terms = np.array(vectorizer.get_feature_names_out())

        scored = vectorizer.transform(texts)
        scores_array = scored.toarray()
        results.append({})

        for i, row in enumerate(scores_array):
            word_scores = [
                (terms[i], row[i])
                for i in np.where(row > 0)[0]
            ]
            word_scores_sorted = sorted(
                word_scores,
                key=lambda x: x[1],
                reverse=True
            )
            results[-1][communities[i]] = [
                w[0] for w in word_scores_sorted
            ]

    tfidf_table = pd.DataFrame([
        [
            c,
            ' \\newline '.join(results[0][c][
                :nterms
            ]),
            ' \\newline '.join(results[1][c][
                :nterms
            ])# ,
            # ' \\newline '.join(results[2][c][
            #     :nterms
            # ]),
        ] for i, c in enumerate(sorted(target_communities))
    ])
    tfidf_table.columns = ('Community', 'Top TF-IDF Unigrams', 'Top TF-IDF Bigrams')
    with open('output/tfidf.tex', 'w') as f:
        table = tfidf_table.to_latex(
            index=False,
            column_format="l p{4cm} p{4cm} p{4cm}"
        )
        table = table.replace(
            'midrule', 'hline',
        ).replace(
            'bottomrule', 'hline',
        ).replace(
            'toprule', 'hline',
        )
        f.write(table)


if __name__ == '__main__':
    main()
