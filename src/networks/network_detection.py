import networkx as nx
from nltk import bigrams as find_bigrams, word_tokenize, sent_tokenize, trigrams as find_trigrams
import textwrap
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
mpl.rcParams.update({'font.size': 18})
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import os
import sys
from config import(
    RESOLUTION,
    TOP_N,
    n_terms_for_table as n_terms,
    N_INITIAL_COMMUNITIES,
    N_TFIDF_LABEL,
    colors,
    MIN_COMMUNITY_PAPERS,
    tables_dests,
    graph_dests,
    stop,
    delete_title,
    background_color,
    text_color
)

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


def cleanup():
    """Must be run the first time that networks are made"""
    session = SessionFactory()
    delete_papers = session.query(Paper).filter(
        func.lower(Paper.title)==delete_title.lower()
    ).all()
    assert(len(delete_papers) in (22, 0))
    [session.delete(p) for p in delete_papers]
    session.commit()

def label_papers_by_community(resolution=RESOLUTION):
    #cleanup()
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

def community_tfidf(n=1):
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
    vectorizer = TfidfVectorizer(
        stop_words=stop,
        ngram_range=(1,2),
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
    def make_label(terms, n=2):
        label = ''
        for i, term in enumerate(terms):
            if i == n:
                label = f'{label}\n'
            label = f'{label}{term}, '            
        return label[:-2]
            
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
            new_name =': '.join(
                (
                    str(int(plotdf.columns[i])),
                    make_label([
                        tfidf
                        for tfidf in community_to_tfidf[column]
                    ][:N_TFIDF_LABEL])
                )
            )
            plotdf.rename(
                columns={
                    plotdf.columns[i]: f'#{new_name}'
                },
                inplace=True
            )

    fig, ax = plt.subplots(figsize=(8,6))
    axes = [ax]
    fig.patch.set_facecolor(background_color)
    plotdf.plot(        
        kind="area",
        stacked=True,
        color=colors,
        ax=ax,
        xlabel='Year',
        ylabel='# of papers',
    )

    tables = []
    tfidf_table = pd.DataFrame({
        'Community': [
            c for c in communities
        ],
        f'TF-IDF (unigram-trigram)': [
            ', '.join(community_to_tfidf[c][:n_terms])
            for c in communities
        ]
        # f'Top bigrams': [
        #     ', '.join(community_to_bigrams[c][:n_terms])
        #     for c in communities
        # ],
        # f'Top trigrams': [
        #     ', '.join(community_to_trigrams[c][:n_terms])
        #     for c in communities
        # ],
    })
    tables.append(tfidf_table)
    
    with open(tables_dests[0], 'w') as f:
        f.write(
            tfidf_table.to_latex(index=False)
        )
        
    # ============= #
    # TODO: lots of repeated code below
    # that should be consolidated.
    # It runs the same analysis as above
    # but on a single year
    # ============= #

    communities = []
    year = 2023
    annual_comm = (
        session.query(
            Paper.community,
            functions.count(Paper.doi),
        ).
        filter(Paper.year==int(year)).                
        group_by(Paper.community).
        having(
            functions.count(Paper.doi)
            >
            min_group_count
        ).
        order_by(
            desc(functions.count(Paper.doi)),
        )
    ).all()

    communities.extend([
        c[0] for c in annual_comm
    ])

    communities = communities[:n_initial_communities]
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

    fig, ax = plt.subplots(figsize=(8,6))
    axes.append(ax)
    fig.patch.set_facecolor(background_color)

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
            new_name =': '.join(
                (
                    str(int(plotdf.columns[i])),
                    make_label([
                        tfidf
                        for tfidf in community_to_tfidf[column]
                    ][:N_TFIDF_LABEL])
                )
            )
            plotdf.rename(
                columns={
                    plotdf.columns[i]: f'#{new_name}'
                },
                inplace=True
            )            
    
    plotdf.plot(        
        kind="area",
        stacked=True,
        color=colors,
        ax=ax,
        xlabel='Year',
        ylabel='# of papers',
        
    )

    print(axes)
    for i, ax in enumerate(axes):
        # ax.xaxis.label.set_fontsize(22)
        # ax.yaxis.label.set_fontsize(22)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        print('here1')
        ax.set_facecolor(background_color)
        ax.tick_params(colors=text_color)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        leg = ax.get_legend()
        leg.get_frame().set_facecolor(background_color)
        leg.get_frame().set_edgecolor(background_color)
        leg.get_frame().set_edgecolor(background_color)
        leg.get_frame().set_alpha(0)
        for text in leg.get_texts():
            text.set_color(text_color)
            text.set_fontsize(14)
        for spine in ax.spines.values():
            spine.set_color(text_color)

        ax.set_xlabel("Year", fontsize=16)
        ax.set_ylabel("# of Papers", fontsize=16)
        ax.tick_params(labelsize=14)

        plt.tight_layout()
        fig = ax.get_figure()
        fig.savefig(graph_dests[i])                    
    
    
    tfidf_table = pd.DataFrame({
        'Community': [
            c for c in communities
        ],
        f'TF-IDF (unigram-trigram)': [
            ', '.join(community_to_tfidf[c][:n_terms])
            for c in communities
        ],
        # f'Top bigrams': [
        #     ', '.join(community_to_bigrams[c][:n_terms])
        #     for c in communities
        # ],
        # f'Top trigrams': [
        #     ', '.join(community_to_trigrams[c][:n_terms])
        #     for c in communities
        # ],
    })
    tables.append(tfidf_table)
    
    with open(tables_dests[1], 'w') as f:
        f.write(
            tfidf_table.to_latex(index=False)
        )

    tables = pd.concat([tables[0], tables[1]])
    tables = tables.drop_duplicates()
    with open(tables_dests[2], 'w') as f:
        f.write(
            tables.to_latex(index=False)
        )


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
    make_graph(
        top_n=TOP_N,
        n_initial_communities=N_INITIAL_COMMUNITIES,
        relabel=False
    )
            
            
        
        
