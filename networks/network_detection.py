import networkx as nx
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import os
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../database'
    )
)
from models import Paper, Author, SessionFactory


engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)

RESOLUTION=5
MIN_GROUP_SIZE=10


def label_papers_by_community(resolution=RESOLUTION):
    session = SessionFactory()
    G = nx.Graph()
    G.add_nodes_from([
        p.doi for p in session.query(Paper).all()
    ])
            
    for j, author in enumerate(session.query(Author).all()):
        if j % 5000 == 0:
            print(j)
        for i, paper1 in enumerate(author.papers):
            for paper2 in author.papers[i+1:]:
                G.add_edge(paper1.doi, paper2.doi)
                
    communities = nx.algorithms.community.louvain_communities(
        G,
        resolution=resolution
    )
    
    for i, community in enumerate(communities):
        for doi in community:
            
            paper = session.query(Paper).filter(
                Paper.doi==doi
            ).one()
            paper.community = i
            session.add(paper)
            
    session.commit()

def top_tfidf():
    session = SessionFactory()
    texts = (
        session.query(
            functions.concat(
                Paper.title,
                ' ',
                Paper.abstract,
            )
        ).
        group_by(Paper.community).
        order_by(Paper.community)
    ).all()

    texts = [
        ' '.join(str(text[0]).split())
        for text in texts 
    ]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    terms = np.array(vectorizer.get_feature_names_out())

    scored = vectorizer.transform(texts)
    scores_array = scored.toarray()
    results = []

    for row in scores_array:
        word_scores = [(terms[i], row[i]) for i in np.where(row > 0)[0]]
        word_scores_sorted = sorted(word_scores, key=lambda x: x[1], reverse=True)
        results.append(word_scores_sorted)

    return results


def make_graph(min_group_size=MIN_GROUP_SIZE):
    label_papers_by_community()
    session = SessionFactory()
    communities = (
        session.query(
            Paper.community,
        ).
        group_by(Paper.community).
        having(
            functions.count(Paper.doi) > min_group_size
        )
    ).all()
    communities = [
        c[0] for c in communities
    ]

    years = list(set([
        p.year for p in session.query(Paper).all()
    ]))

    data = {}
    papers = session.query(
        Paper.community,
        Paper.year
    ).filter(Paper.community.in_(communities)).all()
    df = pd.DataFrame(papers)
    df.columns = ('community', 'year')
    plotdf = df.groupby('year').apply(
        lambda X: pd.Series({
            community: len(X[X.community==community])
            for community in communities
        })
    ).plot(        
        kind="area",
        stacked=True
    )
    plt.show()
    
    # tfidf = top_tfidf()
    # for paper in papers:
    #     pass
        
        
    


if __name__ == '__main__':
    #label_papers_by_community()
    #results = top_tfidf()
    make_graph(15)
            
            
        
        
