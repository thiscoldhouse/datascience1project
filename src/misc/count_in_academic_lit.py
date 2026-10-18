import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size': 15})

from config import *

def main():
    df = pd.read_csv('input/scopus_citations.csv')
    fig, ax = plt.subplots(
        figsize=(8, 6),
        facecolor=background_color
    )

    df = df.groupby('Year').count().reset_index()[['Year', 'DOI']]

    df['Count'] = df['DOI']
    
    df[['Year', 'Count']].plot(
        ax=ax,
        color=text_color,
        x='Year',
        y='Count',
        xlabel='Year',
        ylabel="Count",
        legend=False,
        lw=3    
    )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_facecolor(background_color)
    ax.tick_params(colors=text_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.axvline(
        2016,
        linestyle=':',
        linewidth=1,
        color=before_color,
        label="November 8, 2016"
    )

    for spine in ax.spines.values():
        spine.set_color(text_color)

    ax.set_xlabel(
        'Date'
    )
    ax.set_ylabel('Count')
    leg = ax.legend()
    leg.get_frame().set_facecolor(background_color) 
    leg.get_frame().set_edgecolor(before_color)

    ax.annotate(
        "Not zero!",
        xy=(2011, 120),
        xytext=(0, 100),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='->', color=before_color),
        fontsize=14,
        color=text_color
    )


    plt.xticks(rotation=45)
    plt.savefig('output/count_in_lit.pdf')

if __name__ == '__main__':
    main()
