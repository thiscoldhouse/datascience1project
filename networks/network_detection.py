import networkx as nx
from nltk import bigrams as find_bigrams, word_tokenize, sent_tokenize, trigrams as find_trigrams
import textwrap
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sqlalchemy import create_engine, desc, func
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

# -- move to config.py -- #
RESOLUTION = 1
TOP_N = 2
n_terms = 10
N_INITIAL_COMMUNITIES = 10
colors = [
    '#DB9D47', '#593C8F', '#1B512D', '#666A86', '#6A041D', '#090446',  '#8CC084', '#E86A92', '#009DDC', '#FFDDD2', '#A72608', '#63D2FF','#433A3F', '#28190E',
]
MIN_COMMUNITY_PAPERS = 10
tables_dests = (
    'output/tables0.md',
    'output/tables1.md'
)
graph_dests = (
    'output/communities-graph.pdf',
    'output/first-communities.pdf'
)

from nltk.corpus import stopwords
stop = stopwords.words('english')
stop.extend((
    'elsevier', 'rights', 'reserved', 'mesh', 'taylor', 'francis', 'copyright', 'llc', 'bt', 'lftb', 'springer', 'ieee', 'information', 'misinformation', 'claimscan', 
))
stop = [w.lower() for w in stop]
delete_title = 'Medical misinformation: vet the message!'

# -- #

def cleanup():
    session = SessionFactory()
    delete_papers = session.query(Paper).filter(
        func.lower(Paper.title)==delete_title.lower()
    ).all()
    assert(len(delete_papers) in (22, 0))
    [session.delete(p) for p in delete_papers]
    session.commit()

def label_papers_by_community(resolution=RESOLUTION):
    """
    Small world

    https://sci-hub.ru/https://doi.org/10.1108/AJIM-09-2014-0116
    """
    cleanup()
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
                
    # rework network to penalize hubs
    G_final = nx.Graph()
    G_final.add_nodes_from([
        p.doi for p in session.query(Paper).all()
    ])
    for u, v in G.edges():
        G_final.add_edge(
            u,
            v,
            weight = 1 / (G.degree[u] * G.degree[v])
        )
                           
    communities = nx.algorithms.community.louvain_communities(   
        G_final,
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

def community_tfidf():
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
        ' '.join(str(text[0]).split()).lower()
        for text in texts 
    ]
    #texts = ['-'.join(b) for b in bigrams(texts)]

    vectorizer = TfidfVectorizer(
        stop_words=stop,
        ngram_range=(1,1),
    )
    X = vectorizer.fit_transform(texts)
    terms = np.array(vectorizer.get_feature_names_out())

    scored = vectorizer.transform(texts)
    scores_array = scored.toarray()
    results = []

    for row in scores_array:
        word_scores = [
            (terms[i], row[i])
            for i in np.where(row > 0)[0]
        ]
        word_scores_sorted = sorted(
            word_scores,
            key=lambda x: x[1],
            reverse=True
        )
        results.append([
            w[0] for w in word_scores_sorted
        ])

    return results


def make_graph(
        top_n=5,
        relabel=False,
        min_group_count=MIN_COMMUNITY_PAPERS,
        n_initial_communities=N_INITIAL_COMMUNITIES
):
    if relabel is True:
        label_papers_by_community()
        
    session = SessionFactory()

    papers = pd.DataFrame(
        session.query(
            Paper.community,
            Paper.year
        ).all()
    )
    papers.columns = ('community', 'year')
    years = papers['year'].unique()
    
    communities = []
    for year in years:
        annual_comm = (
            session.query(
                Paper.community,
                functions.count(Paper.doi),
            ).
            filter(Paper.year==int(year)).                
            group_by(Paper.community).
            having(
                functions.count(Paper.doi) > min_group_count
            ).
            order_by(
                desc(functions.count(Paper.doi)),
            )
        ).all()
        communities.extend([
            c[0] for c in annual_comm[:top_n]
        ])
        
    communities = list(set(communities))
    data = {}
    papers = session.query(
        Paper.community,
        Paper.year
    ).filter(Paper.community.in_(communities)).all()
    df = pd.DataFrame(papers)
    df.columns = ('community', 'year')

    community_to_tfidf = community_tfidf()
    community_to_bigrams = list(
        community_ngrams(ngram_finder=find_bigrams)
    )
    community_to_trigrams = list(
        community_ngrams(ngram_finder=find_trigrams)
    )
    
    plotdf = df.groupby('year').apply(
        lambda X: pd.Series({
            community: len(X[X.community==community])
            for community in communities
        })
    )
    for i, column in enumerate(plotdf.columns):
        if column not in communities:
            del plotdf[column]
        else:
            new_name =': '.join((
                str(int(plotdf.columns[i])),
                ', '.join([
                        tfidf
                        for tfidf in community_to_tfidf[column]
                    ][:5])
            ))
            plotdf.rename(
                columns={
                    plotdf.columns[i]: new_name
                },
                inplace=True
            )            
            

    plotdf.plot(        
        kind="area",
        stacked=True,
        color=colors
    )
    
    tfidf_table = pd.DataFrame({
        'Community': [
            c for c in communities
        ],
        f'TF-IDF': [
            ', '.join(community_to_tfidf[c][:n_terms])
            for c in communities
        ],
        f'Bigrams': [
            ', '.join(community_to_bigrams[c][:n_terms])
            for c in communities
        ],
        f'Trigrams': [
            ', '.join(community_to_trigrams[c][:n_terms])
            for c in communities
        ],
    })
    
    with open(tables_dests[0], 'w') as f:
        f.write(
            tfidf_table.to_markdown(index=False)
        )
        
    plt.savefig(graph_dests[0])
    plt.show()

    # ============= #
    # TODO: lots of repeated code below
    # should be consolidated
    # Uncomment to run the same analysis as
    # above but on a single year
    # ============= #

    # communities = []
    # year = 2023
    # annual_comm = (
    #     session.query(
    #         Paper.community,
    #         functions.count(Paper.doi),
    #     ).
    #     filter(Paper.year==int(year)).                
    #     group_by(Paper.community).
    #     having(
    #         functions.count(Paper.doi)
    #         >
    #         min_group_count
    #     ).
    #     order_by(
    #         desc(functions.count(Paper.doi)),
    #     )
    # ).all()

    # communities.extend([
    #     c[0] for c in annual_comm
    # ])

    # communities = communities[:n_initial_communities]
    # print(communities)
        
    # communities = list(set(communities))
    # data = {}
    # papers = session.query(
    #     Paper.community,
    #     Paper.year
    # ).filter(Paper.community.in_(communities)).all()
    
    # df = pd.DataFrame(papers)
    # df.columns = ('community', 'year')

    # community_to_tfidf = community_tfidf()
    # community_to_bigrams = list(
    #     community_ngrams(ngram_finder=find_bigrams)
    # )
    # community_to_trigrams = list(
    #     community_ngrams(ngram_finder=find_trigrams)
    # )
    
    # plotdf = df.groupby('year').apply(
    #     lambda X: pd.Series({
    #         community: len(X[X.community==community])
    #         for community in communities
    #     })
    # )
    # for i, column in enumerate(plotdf.columns):
    #     if column not in communities:
    #         del plotdf[column]
    #     else:
    #         new_name =': '.join((
    #             str(int(plotdf.columns[i])),
    #             ', '.join([
    #                     tfidf
    #                     for tfidf in community_to_tfidf[column]
    #                 ][:5])
    #         ))
    #         plotdf.rename(
    #             columns={
    #                 plotdf.columns[i]: new_name
    #             },
    #             inplace=True
    #         )            
            
    # plotdf.plot(        
    #     kind="area",
    #     stacked=True,
    #     color=colors
    # )
    # tfidf_table = pd.DataFrame({
    #     'Community': [
    #         c for c in communities
    #     ],
    #     f'TF-IDF': [
    #         ', '.join(community_to_tfidf[c][:n_terms])
    #         for c in communities
    #     ],
    #     f'Bigrams': [
    #         ', '.join(community_to_bigrams[c][:n_terms])
    #         for c in communities
    #     ],
    #     f'Trigrams': [
    #         ', '.join(community_to_trigrams[c][:n_terms])
    #         for c in communities
    #     ],
    # })
    
    # with open(tables_dests[1], 'w') as f:
    #     f.write(
    #         tfidf_table.to_markdown(index=False)
    #     )
        
    # plt.savefig(graph_dests[1])
    # plt.title(f'Top {n_initial_communities} communities from year {year}')
    # plt.show()


        
def community_ngrams(ngram_finder=None):
    if ngram_finder is None:
        ngram_finder = find_bigrams
        
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
    
    for text in texts:
        text = text[0]
        result = ngram_finder(word_tokenize(text.lower()))
        bigrams = []
        for bg in result:
            if any([
                word in stop for word in bg
            ]) or any([
                not word.isalpha() for word in bg                
            ]):
                continue            
            bigrams.append(' '.join(bg))
            
        bigrams = sorted(
            ((s, bigrams.count(s)) for s in set(bigrams)), 
            key=lambda x: -x[1]
        )
        yield [b[0] for b in bigrams]


        
if __name__ == '__main__':
    make_graph(top_n=TOP_N, n_initial_communities=N_INITIAL_COMMUNITIES, relabel=False)
            
            
        
        
