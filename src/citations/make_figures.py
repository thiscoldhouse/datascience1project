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
from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from matplotlib.colors import LinearSegmentedColormap
from config import *

engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)


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

    fig, axes = plt.subplots(
        1, 2,
        figsize=(18, 9),
        facecolor=background_color
    )
    ax1, ax2 = axes
    
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

    # ======== graph ========= #
    
    G = nx.DiGraph()
    G.add_nodes_from(
        flow['source_comm'].unique()
    )
    for row in flow.iterrows():
        G.add_edge(
            int(row[1].source_comm),
            int(row[1].target_comm),
            weight=int(row[1].weight)
        )

    pos = nx.circular_layout(G)
    node_sizes = [
        len(
            session.query(Paper.doi).filter(
                Paper.community==int(c)
            ).all()
        ) for c in G.nodes()        
    ]
    node_sizes = [
        int(s * 22)
        for s in node_sizes
    ]
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax1,
        node_color= [
            before_color if int(node) != 1432 else after_color
            for node in G.nodes()
        ],
        node_size=node_sizes,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        ax=ax1,
        font_size=22,
        font_color="black"
    )
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    weights = [
        np.log(w)  for w in weights
    ]    
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax1,
        arrows=True,
        width=weights,
        arrowsize=20,
        min_source_margin=20,
        min_target_margin=20,
        connectionstyle='arc3,rad=0.3',
        edge_color=text_color
    )
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

    
if __name__ == "__main__":
    citation_flows()
