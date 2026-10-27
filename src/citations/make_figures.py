import os
import sys

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../database'
    )
)
import matplotlib
import matplotlib.pyplot as plt
from models import Paper, Author, Citation
import pandas as pd
import numpy as np
import networkx as nx
import sqlite3 
from sqlalchemy import create_engine, and_, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from matplotlib.colors import LinearSegmentedColormap
from config import *
import plotly.graph_objects as go

engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)

def most_cited(rebuild=False):
    if not rebuild:
        return pd.read_csv('output/top_cited_authors.csv')
        
    session = SessionFactory()
    citations = pd.DataFrame([
        {
            'cited': c.cited.doi,
            'citing': c.citing.doi,
            'year': c.cited.year,
            'title': c.cited.title,
        }
        for c in session.query(Citation).all()
        if c.cited.doi is not None and c.cited.doi != ''
    ])
    
    citations = citations.groupby([
        'cited', 'year', 'title'
    ]).count().reset_index()
    authors = []
    for author in session.query(Author).all():
        for paper in author.papers:
            authors.append(
                {
                    'doi': paper.doi,
                    'name': author.name,
                    'id': author.id
                }
            )
    authors = pd.DataFrame(authors)
    authors = authors.merge(
        citations[['cited', 'citing']],
        left_on='doi',
        right_on='cited'
    )
    authors_count = authors[['doi', 'name', 'citing', 'id']].groupby([
        'id', 
    ]).sum('citing').reset_index()
    citations.to_csv('output/in_progress/citations_df.csv')
    authors.to_csv('output/in_progress/authors_df.csv')
    authors_count.to_csv('output/in_progress/authors_count_df.csv')    
    df = authors_count.sort_values(
        'citing', ascending=False
    ).merge(
        authors[['id', 'name']].drop_duplicates(
            subset=['id', 'name']
        ), on='id'
    )
    df.to_csv('output/top_cited_authors.csv')
    return df


def citation_flows():
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
                functions.count(Paper.doi) >
                MIN_COMMUNITY_PAPERS
            ).
            order_by(
                desc(functions.count(Paper.doi)),
            )
        ).all()
        communities.extend([
            c[0] for c in annual_comm[:TOP_N]
        ])
        
    communities = sorted(list(set(communities)))

    papers = pd.DataFrame([
        (p.doi, p.community)
        for p in session.query(Paper).filter(
                Paper.community.in_(communities)
        ).all()
    ])    
    papers.columns = ('doi', 'community',)

    citations = pd.DataFrame([
        (
            c.citing_paper_doi,
            c.cited_paper_doi,
        ) for c in session.query(Citation).all()
    ])
    citations.columns = ('citing_paper_doi', 'cited_paper_doi')

    left = pd.merge(
        citations,
        papers,
        left_on='citing_paper_doi',
        right_on='doi',
        how="inner"
    ).rename(
        columns={'community': "source_comm"}
    ).drop(
        columns=['doi']
    )

    merged = pd.merge(
        left,
        papers,
        left_on='cited_paper_doi',
        right_on='doi',
        how="inner"
    ).rename(
        columns={'community': "target_comm"}
    ).drop(
        columns=['doi']
    )

    merged = merged.sort_values('source_comm')

    flow = merged.groupby(
        ['source_comm', 'target_comm']
    ).size().reset_index(name='weight')

    # fig, axes = plt.subplots(
    #     1, 2,
    #     figsize=(18, 9),
    #     facecolor=background_color
    # )
    # ax1, ax2 = axes

    fig, ax2 = plt.subplots(figsize=(12,10))
    axes = [ax2]
    # ========= heatmap ====== #

    heatmapdf = flow.pivot_table(
        index="target_comm",
        columns="source_comm",
        values="weight",
        fill_value=0
    )    
    heatmapdf = heatmapdf.sort_index().sort_index(axis=1)
    im = ax2.imshow(
        heatmapdf.values,
        cmap=LinearSegmentedColormap.from_list(
            'custom',
            color_map_colors
        )
    )
    ax2.set_xticks(np.arange(heatmapdf.shape[1]))
    ax2.set_yticks(np.arange(heatmapdf.shape[0]))
    ax2.set_xticklabels(heatmapdf.columns)
    ax2.set_yticklabels(heatmapdf.index)
    matplotlib.rcParams.update({'font.size': 24})
    plt.setp(
        ax2.get_xticklabels(),
        rotation=45,
        ha="right",
        rotation_mode="anchor",
    )
    for i in range(heatmapdf.shape[0]):
        for j in range(heatmapdf.shape[1]):
            text = ax2.text(
                j,
                i,
                int(heatmapdf.values[i, j]),
                ha="center",
                va="center",
                color=text_color,
            )

    cbar = ax2.figure.colorbar(im, ax=ax2)
    cbar.set_label("Citations", color=text_color)
    cbar.ax.yaxis.set_tick_params(
        color=text_color,
        labelcolor=text_color,
        labelsize=18,
    )
    for spine in cbar.ax.spines.values():
        spine.set_edgecolor(text_color)
        spine.set_linewidth(2)

    ax2.set_xlabel("Source Community", fontsize=24)
    ax2.set_ylabel("Target Community", fontsize=24)
    ax2.set_title("Citations: Source to Target", fontsize=24)

    # # ======== graph ========= #
    
    # G = nx.DiGraph()
    # G.add_nodes_from(
    #     flow['source_comm'].unique()
    # )
    # for row in flow.iterrows():
    #     G.add_edge(
    #         int(row[1].source_comm),
    #         int(row[1].target_comm),
    #         weight=int(row[1].weight)
    #     )

    # pos = nx.circular_layout(G)
    # node_sizes = [
    #     len(
    #         session.query(Paper.doi).filter(
    #             Paper.community==int(c)
    #         ).all()
    #     ) for c in G.nodes()        
    # ]
    # node_sizes = [
    #     int(s * 22)
    #     for s in node_sizes
    # ]
    # nx.draw_networkx_nodes(
    #     G,
    #     pos,
    #     ax=ax1,
    #     node_color= [
    #         before_color if int(node) != 1432 else after_color
    #         for node in G.nodes()
    #     ],
    #     node_size=node_sizes,
    # )
    # nx.draw_networkx_labels(
    #     G,
    #     pos,
    #     ax=ax1,
    #     font_size=22,
    #     font_color="black"
    # )
    # weights = [G[u][v]["weight"] for u, v in G.edges()]
    # weights = [
    #     np.log(w)  for w in weights
    # ]    
    # nx.draw_networkx_edges(
    #     G,
    #     pos,
    #     ax=ax1,
    #     arrows=True,
    #     width=weights,
    #     arrowsize=20,
    #     min_source_margin=20,
    #     min_target_margin=20,
    #     connectionstyle='arc3,rad=0.3',
    #     edge_color=text_color
    # )
    for ax in axes:
        for spine in ax.spines.values():
            spine.set_color(text_color)        

        ax.set_facecolor(background_color)
        ax.title.set_color(text_color)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.tick_params(colors=text_color, labelsize=20)
        for ax in axes:
            leg = ax.get_legend()
            if leg is None:
                continue
            for text in leg.get_texts():
                text.set_color(text_color)
    
    plt.savefig(dest)

def make_tables(c2s, c1=1432):
    df = pd.DataFrame({
        'Year of Source Paper': [],
        'Year of Target Paper': [],
        'Source Paper': [],
        'Target Paper': []
    })
    for i,c2 in enumerate(c2s):
        sql = f'''
            select
            p2.year as 'Year of Source Paper',
            p1.year as 'Year of Target Paper',
            p2.title as 'Source Paper',
            p1.title as 'Target Paper'
            from paper p1
            inner join citation c
            on c.cited_paper_doi = p1.doi
            inner join paper p2
            on p2.doi = citing_paper_doi
            where p1.community={c1}
            and p2.community={c2}
            order by p2.year;
        '''

        thisdf = pd.read_sql_query(
            sql,
            sqlite3.connect('input/papers.db')
        )
        df = pd.concat([
            df,
            thisdf.loc[list(table_rows[i])].reset_index()
        ])

    df['Year of Source Paper'] = df['Year of Source Paper'].astype(int)
    df['Year of Target Paper'] = df['Year of Target Paper'].astype(int)    
    with open(f'output/example_citations.tex', 'w') as f:
        f.write(
            df[['Source Paper', 'Target Paper']].to_latex(
                index=False,
                column_format=('p{.49\\textwidth}p{.49\\textwidth}'))
        )

def make_most_cited_table(df):
    df = df[['citing', 'name']][:10]
    names_and_affils = None
    with open('name_and_affiliation.csv', 'r') as f:
        names_and_affils = [
            [cell.strip() for cell in row.split('|')]
            for row in f.read().split('\n')
            if row
        ]
    name_map = {row[0]:row[1] for row in names_and_affils}
    print(name_map)
    df['name'] = df['name'].apply(
        lambda n: name_map[n.strip()]
    )
    df['affiliation'] = [row[2] for row in names_and_affils][:10]
    with open('output/most_cited_authors.tex', 'w') as f:
        df.columns = [
            'Citation Count', 'Name', 'Affiliation'
        ]
        table = df.to_latex()
        table = table.replace(
            'toprule', 'hline'
        ).replace(
            'midrule', 'hline'
        ).replace(
            'bottomrule', 'hline'
        )
        f.write(table)

def sankey(min_comm=1):
    session = SessionFactory()
    papers = pd.DataFrame([
        {
            'auth_comm': f'Authorship:{paper.community}',
            'cit_comm': f'Citation:{paper.citation_community}',
            'id': paper.doi
        }
        for paper in session.query(Paper).all()
    ])
    print(len(papers))
    papers = papers.groupby(['auth_comm', 'cit_comm']).size()
    papers = papers.reset_index()
    papers.columns = ('auth_comm', 'cit_comm', 'count')
    
    filter_comms = papers.groupby(
            'auth_comm'
    ).size().reset_index()
    filter_comms.columns = ('auth_comm', 'count')
    filter_comms = filter_comms[filter_comms['count'] > min_comm]
    papers = papers[
        papers.auth_comm.isin(filter_comms['auth_comm'])
    ]

    filter_comms = papers.groupby(
            'cit_comm'
    ).size().reset_index()
    filter_comms.columns = ('cit_comm', 'count')
    filter_comms = filter_comms[filter_comms['count'] > min_comm]
    papers = papers[
        papers.cit_comm.isin(filter_comms['cit_comm'])
    ]

    print(len(papers))
    print(papers[papers.auth_comm==1432])
    all_nodes = papers['auth_comm'].tolist() + papers['cit_comm'].tolist()
    node_index = {name: i for i, name in enumerate(all_nodes)}
    sources = papers['auth_comm'].map(node_index).tolist()
    targets = papers['cit_comm'].map(node_index).tolist()
    values = papers['count'].tolist()

    fig = go.Figure(data=[go.Sankey(
        orientation='v',
        node=dict(
            label=all_nodes,
            pad=20,
            thickness=20,
            line=dict(width=0.5)
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )])

    fig.update_layout(
        title_text="Communities",
        font_size=10,
        height=800,
        width=1200
    )
    fig.show()

def community_correspondance(
        top_n=10
):
    session = SessionFactory()
    df = pd.DataFrame([
        {
            'auth_comm': f'Authorship:{paper.community}',
            'cit_comm': f'Citation:{paper.citation_community}',
            'id': paper.doi
        }
        for paper in session.query(Paper).all()
        if paper.community is not None and paper.citation_community is not None
    ])
    filter_auth_comms = (
        df.groupby('auth_comm').
        size().
        rename('size').
        reset_index().
        sort_values('size', ascending=False)
    ).head(top_n)['auth_comm'].tolist()
    
    counts = (
        df.groupby(['auth_comm', 'cit_comm'])
          .size()
          .rename('count')
          .reset_index()
    )
    counts = counts[counts.auth_comm.isin(filter_auth_comms)]
    counts = counts.sort_values('count', ascending=False)
    counts['fraction'] = (
        counts['count'] /
        counts.groupby('auth_comm')['count'].transform('sum')
    )
    counts['rank'] = (
        counts.groupby('auth_comm')['count']
              .rank(method='first', ascending=False)
    )
    counts = counts[counts['rank'] <= 3].copy()
    table = []    
    for auth_comm in counts['auth_comm'].unique():
        row = []
        row.append(auth_comm)
        for i, this_row in enumerate(
                counts[
                    counts.auth_comm == auth_comm
                ].values.tolist()
        ):
            if i > 2:
                raise ValueError('Failed sanity check')
            row.extend((this_row[1], this_row[3]))
        table.append(row)

    new_table = []
    for row in table:
        if row is None:
            continue
        if len(row) == 3:
            row.extend((None, None))
        if len(row) == 5:
            row.extend((None, None))

        row.append(
            (row[2] or 0)
            +
            (row[4] or 0)
            +
            (row[6] or 0)
        )            

        row[-1] = round(row[-1], 2)
        new_table.append(row)

    with open('output/correspondance.tex', 'w') as f:
        table = pd.DataFrame(table)
        table.columns = [
            'Author community',
            'First citation community',
            'Overlap with first citation community',
            'Second citation community',
            'Ovelap with second citation community',
            'Third citation community',
            'Overlap with third citation community',
            'Sum of top three'
        ]
        table = table[[
            'Author community',
            'Overlap with first citation community',
            'Ovelap with second citation community',
            'Overlap with third citation community',
            'Sum of top three'
        ]].sort_values('Sum of top three', ascending=False)
        table['Author community'] = table['Author community'].apply(
            lambda x: x.replace('Authorship:', '')
        )
        table = table.to_latex(
            index=False,
            float_format="%.2f",
            column_format='p{.1\\textwidth}' * 9
        )
        table = table.replace(
            'toprule', 'hline'
        ).replace(
            'midrule', 'hline'
        ).replace(
            'bottomrule', 'hline'
        )
        table = table.replace('NaN', 'N/A')
        f.write(table)
        with open('output/debugging_table.tex', 'w') as g:
            template = '''
            \\documentclass{article}
            \\usepackage[margin=1in]{geometry}
            \\usepackage{graphicx}            
            \\begin{document}
            TABLE
            \\end{document}
            '''
            g.write(template.replace('TABLE', table))

        
if __name__ == "__main__":
    #citation_flows()
    #make_tables(table_data)
    # make_most_cited_table(
    #     most_cited(rebuild=False)
    # )
    #sankey()
    community_correspondance()
