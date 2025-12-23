from config import(
    background_color,
    before_color,
    before_color,
    text_color
)
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size': 18})
import os
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../database'
    )
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Paper, Author, SessionFactory


engine = create_engine(
    "sqlite:///input/papers.db",
)
SessionFactory = sessionmaker(bind=engine)

def reformat_title(title, n=4):
    new_title = ''
    for i, word in enumerate(title.split()):
        if i > 0 and i%n == 0:
            new_title = f'{new_title}\n{word}'
        else:
            new_title = f'{new_title} {word}'

    return new_title.strip()


def axconfig(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_facecolor(background_color)
    ax.tick_params(colors=text_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    
    for spine in ax.spines.values():
        spine.set_color(text_color)
            
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("# of Papers", fontsize=14)
    ax.tick_params(labelsize=14)    



def make_graph1(community=4645):
    dest = f'output/{community}.pdf'
    session = SessionFactory()
    papers = session.query(Paper).filter(
        Paper.community==community
    ).all()
    papers = sorted(
        papers,
        key=lambda p: p.year
    )
    fig, ax = plt.subplots(figsize=(7,6))
    fig.patch.set_facecolor(background_color)
    counts = pd.Series([
        p.year for p in papers
    ]).value_counts().sort_index()
    counts.plot(
        ax=ax,
        color=text_color,
        marker='o',
        markersize=5,
        markerfacecolor=text_color,
        markeredgecolor=text_color,
        markeredgewidth=0.5,
        legend=False,
        lw=3
    )
    
    ax.annotate(
        reformat_title(papers[0].title, n=2),
        xy=(papers[0].year, len([
            p for p in papers if p.year==papers[0].year
        ])),
        xytext=(-10, 100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[1].title),
        xy=(papers[1].year, len([
            p for p in papers if p.year==papers[1].year
        ])),
        xytext=(-95, 200),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[2].title, n=3),
        xy=(papers[2].year, len([
            p for p in papers if p.year==papers[2].year
        ])),
        xytext=(-35, 100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )

    ax.annotate(
        reformat_title(papers[10].title, n=2),
        xy=(papers[10].year, len([
            p for p in papers if p.year==papers[10].year
        ])),
        xytext=(18, -10),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[22].title,n=2),
        xy=(papers[22].year, len([
            p for p in papers if p.year==papers[22].year
        ])),
        xytext=(-40, 50),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    axconfig(ax)
    plt.savefig(dest)


def make_graph2(community=1085):
    dest = f'output/{community}.pdf'
    session = SessionFactory()
    papers = session.query(Paper).filter(
        Paper.community==community
    ).all()
    papers = sorted(
        papers,
        key=lambda p: p.year
    )
    fig, ax = plt.subplots(figsize=(7,6))
    fig.patch.set_facecolor(background_color)
    counts = pd.Series([
        p.year for p in papers
    ]).value_counts().sort_index()
    counts.plot(
        ax=ax,
        color=text_color,
        marker='o',
        markersize=5,
        markerfacecolor=text_color,
        markeredgecolor=text_color,
        markeredgewidth=0.5,
        legend=False,
        lw=3
    )
    
    ax.annotate(
        reformat_title(papers[0].title, n=2),
        xy=(papers[0].year, len([
            p for p in papers if p.year==papers[0].year
        ])),
        xytext=(-5, 50),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[1].title),
        xy=(papers[1].year, len([
            p for p in papers if p.year==papers[1].year
        ])),
        xytext=(-40, 200),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[2].title, n=3),
        xy=(papers[2].year, len([
            p for p in papers if p.year==papers[2].year
        ])),
        xytext=(-15, 90),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )

    # ax.annotate(
    #     reformat_title(papers[10].title),
    #     xy=(papers[10].year, len([
    #         p for p in papers if p.year==papers[10].year
    #     ])),
    #     xytext=(60, -20),
    #     textcoords='offset points',
    #     arrowprops=dict(arrowstyle='->', color=before_color),
    #     fontsize=12,
    #     color=text_color
    # )
    ax.annotate(
        reformat_title(papers[22].title,n=3),
        xy=(papers[22].year, len([
            p for p in papers if p.year==papers[22].year
        ])),
        xytext=(5, -100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    ax.annotate(
        reformat_title(papers[-2].title, n=3),
        xy=(papers[-2].year, len([
            p for p in papers if p.year==papers[-2].year
        ])),
        xytext=(-210, 100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    axconfig(ax)
    plt.savefig(dest)


def make_graph3(community=1432):
    dest = f'output/{community}.pdf'
    session = SessionFactory()
    papers = session.query(Paper).filter(
        Paper.community==community
    ).all()
    papers = sorted(
        papers,
        key=lambda p: p.year
    )
    fig, ax = plt.subplots(figsize=(7,6))
    fig.patch.set_facecolor(background_color)
    counts = pd.Series([
        p.year for p in papers
    ]).value_counts().sort_index()
    counts.plot(
        ax=ax,
        color=text_color,
        marker='o',
        markersize=5,
        markerfacecolor=text_color,
        markeredgecolor=text_color,
        markeredgewidth=0.5,
        legend=False,
        lw=3
    )
    
    ax.annotate(
        reformat_title(papers[0].title, n=3),
        xy=(papers[0].year, len([
            p for p in papers if p.year==papers[0].year
        ])),
        xytext=(0, 90),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[10].title),
        xy=(papers[10].year, len([
            p for p in papers if p.year==papers[10].year
        ])),
        xytext=(0, -200),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[20].title),
        xy=(papers[20].year, len([
            p for p in papers if p.year==papers[20].year
        ])),
        xytext=(0, 100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )

    ax.annotate(
        reformat_title(papers[30].title),
        xy=(papers[30].year, len([
            p for p in papers if p.year==papers[30].year
        ])),
        xytext=(20, -150),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[-100].title,n=4),
        xy=(papers[-100].year, len([
            p for p in papers if p.year==papers[-100].year
        ])),
        xytext=(-50, 50),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[-90].title,n=4),
        xy=(papers[-90].year, len([
            p for p in papers if p.year==papers[-90].year
        ])),
        xytext=(40, 0),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    ax.annotate(
        reformat_title(papers[-20].title,n=3),
        xy=(papers[-20].year, len([
            p for p in papers if p.year==papers[-20].year
        ])),
        xytext=(5, -100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    ax.annotate(
        reformat_title(papers[-2].title,n=3),
        xy=(papers[-2].year, len([
            p for p in papers if p.year==papers[-2].year
        ])),
        xytext=(-250, -30),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    axconfig(ax)
    plt.savefig(dest)
        
def make_graph4(community=6075):
    dest = f'output/{community}.pdf'
    session = SessionFactory()
    papers = session.query(Paper).filter(
        Paper.community==community
    ).all()
    papers = sorted(
        papers,
        key=lambda p: p.year
    )
    fig, ax = plt.subplots(figsize=(7,6))
    fig.patch.set_facecolor(background_color)
    counts = pd.Series([
        p.year for p in papers
    ]).value_counts().sort_index()
    counts.plot(
        ax=ax,
        color=text_color,
        marker='o',
        markersize=5,
        markerfacecolor=text_color,
        markeredgecolor=text_color,
        markeredgewidth=0.5,
        legend=False,        
        lw=3
    )
    
    ax.annotate(
        reformat_title(papers[0].title, n=3),
        xy=(papers[0].year, len([
            p for p in papers if p.year==papers[0].year
        ])),
        xytext=(0, 90),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[10].title),
        xy=(papers[10].year, len([
            p for p in papers if p.year==papers[10].year
        ])),
        xytext=(-70, 200),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[20].title),
        xy=(papers[20].year, len([
            p for p in papers if p.year==papers[20].year
        ])),
        xytext=(-100, 150),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )

    ax.annotate(
        reformat_title(papers[30].title),
        xy=(papers[30].year, len([
            p for p in papers if p.year==papers[30].year
        ])),
        xytext=(20, -150),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[-100].title,n=4),
        xy=(papers[-100].year, len([
            p for p in papers if p.year==papers[-100].year
        ])),
        xytext=(-260, 50),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    ax.annotate(
        reformat_title(papers[-90].title,n=4),
        xy=(papers[-90].year, len([
            p for p in papers if p.year==papers[-90].year
        ])),
        xytext=(-10, 20),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    ax.annotate(
        reformat_title(papers[-20].title,n=3),
        xy=(papers[-20].year, len([
            p for p in papers if p.year==papers[-20].year
        ])),
        xytext=(-20, -100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    ax.annotate(
        reformat_title(papers[-2].title,n=3),
        xy=(papers[-2].year, len([
            p for p in papers if p.year==papers[-2].year
        ])),
        xytext=(-150, -30),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=12,
        color=text_color
    )
    
    axconfig(ax)
    plt.savefig(dest)
        
if __name__ == '__main__':
    make_graph1()
    make_graph2()
    make_graph3()
    make_graph4()
