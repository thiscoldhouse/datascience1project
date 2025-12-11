import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../database'
    )
)
import json
from models import Paper, Author, Citation
import pandas as pd
from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import sessionmaker
from nltk.tokenize import MWETokenizer, word_tokenize

bigrams = [('social', 'media'), ('fake', 'news')]

engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)

def main():
    session = SessionFactory()
    times = ['Before', 'After']
    year_ranges = [
        [2011, 2012, 2013, 2014, 2015],
        [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    ]
    papers = session.query(Paper).filter(
        Paper.community==1432
    ).all()
    for i, time in enumerate(times):
        years = year_ranges[i]
        texts = [
            '. '.join((p.title, p.abstract)).lower()
            for p in papers         
            if p.year in years
        ]

        tokenizer = MWETokenizer(bigrams, separator="_")
        text = '. '.join(texts).replace('©', '').replace('®', '')
        text = word_tokenize(text)
        text = tokenizer.tokenize(text)
        totalunique = len(set(text))
        loop_data = (
            pd.DataFrame({'text': text}).
            groupby('text').
            size().
            reset_index().
            sort_values(0, ascending=False)
        )
        data = []
        years = year_ranges[0]
        years.extend(year_ranges[1])
        years = [str(y) for y in years]
        for row in loop_data.values:
            token, count = row            
            if token in years:
                continue
            data.append({
                'types': token,
                'counts': count,
                'totalunique': totalunique,
                'probs': count / totalunique
            })

        with open(
                f'./output/{time}.json',
                'w'
        ) as f:
            f.write(json.dumps(data))

    f1 = f'./output/{times[0]}.json'
    f2 = f'./output/{times[1]}.json'
    output = './output/allotax.pdf'
    alpha = .1
    cmd = f'python -m py_allotax.generate_svg {f1} {f2} {output} "{alpha}" "Before 2016" "After 2016" --desired_format "pdf"'
    os.system(cmd)

        
if __name__ == '__main__':
    main()
