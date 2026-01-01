import os
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../database'
    )
)
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Paper, Author
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size': 15})

from config import *

engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)

def zipf():
    session = SessionFactory()
    communities = (
        session.query(
            Paper.community,
            func.count(Paper.doi),
        ).
        group_by(
            Paper.community,
        ).
        having(
            func.count(Paper.doi) > 1
        )
    ).all()

    communities = sorted(
        communities,
        key=lambda row: row[-1],
        reverse=True
    )
    ranks = []
    counts = []
    for i, community in enumerate(communities):
        ranks.append(i+1)
        counts.append(community[1])
        
    fig, ax = plt.subplots(
        figsize=(7,6),
        facecolor=background_color
    )
    ax.set_facecolor(background_color)

    for spine in ax.spines.values():
        spine.set_color(text_color)

    ax.tick_params(colors=text_color)
    ax.scatter(
        ranks,
        counts,
        color=text_color,
        s=1
    )
    ax.set_xlabel("Rank", fontsize=14, color=text_color)
    ax.set_ylabel("Frequency", fontsize=14, color=text_color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    log_r = np.log(ranks)
    log_v = np.log(counts)
    slope, intercept = np.polyfit(
        log_r, log_v, 1
    )
    fit_y = np.exp(intercept) * ranks ** slope
    ax.plot(
        ranks,
        fit_y,
        linestyle='--',
        color=before_color,
        linewidth=1,
        label=f'slope = {round(slope, 2)}'
    )
    leg = ax.legend()
    leg.get_frame().set_facecolor(background_color) 
    leg.get_frame().set_edgecolor(before_color)

    for text in leg.get_texts():
        text.set_color(text_color)
    
    # ax.grid(
    #     which="major",
    #     linestyle="--",
    #     linewidth=0.3,
    #     alpha=0.3,
    #     color=text_color
    # )
    
    ax.set_xscale("log")
    ax.set_yscale("log")
        
    ax.set_xlabel('Rank', color=text_color)
    ax.set_ylabel('Count', color=text_color)
    ax.set_title('Rank vs. Size for Communities',
                 color=text_color)
    ax.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig('output/zipf.pdf')

if __name__ == '__main__':
    zipf()
