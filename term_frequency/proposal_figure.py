
import pandas as pd
import numpy as np
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec

from config import (
    before_color,
    after_color,
    before_years,
    after_years,
    stop
)


def tokenize(text):
    return [
        w.lower()
        for w in nltk.word_tokenize(text)
        if w.isalpha() and w.lower() not in stop
    ]    


def top_bigrams(text, top_n_bigrams=50, min_freq=25):
    words = tokenize(text)
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(min_freq)
    scored = finder.score_ngrams(bigram_measures.pmi)
    if scored is None:
        return []
    top_bigrams = set([
        tuple(b[0]) for b in scored[:top_n_bigrams]
    ])
    return top_bigrams


def clean_text_with_bigrams(text,                            
                            top_n_bigrams=200,
                            min_freq=10,
                            top_bigrams_list=None):
    
    if top_bigrams_list is None:
        top_bigrams_list = top_bigrams(
            text,
            top_n_bigrams=top_n_bigrams,
            min_freq=min_freq
        )

    result = []
    i = 0
    words = tokenize(text)
    while i < len(words):
        if (
                i+1 < len(words) and
                (words[i], words[i+1]) in top_bigrams_list
        ):
            result.append(words[i] + ' ' + words[i+1])
            i += 2
        else:
            result.append(words[i])
            i += 1
            
    return result


def get_highest_divergence_terms(
        df,
        before_years,
        after_years,
        topn
):
    bow1 = df[df['Year'].isin(before_years)]
    bow2 = df[df['Year'].isin(after_years)]

    fullbow = ' '.join(df['text'] + df['text'])
    top_bigrams_list = top_bigrams(
        fullbow,
        top_n_bigrams=100,
        min_freq=100,
    )
    bow1 = pd.DataFrame({
        'words': clean_text_with_bigrams(
            ' '.join(bow1['text']), top_bigrams_list=top_bigrams_list
        )
    })
    bow2 = pd.DataFrame({
        'words': clean_text_with_bigrams(
            ' '.join(bow2['text']), top_bigrams_list=top_bigrams_list
        )
    })    

    bow1 = bow1.groupby('words').size().reset_index()
    bow1.columns = ('words', 'count')
    bow2 = bow2.groupby('words').size().reset_index()
    bow2.columns = ('words', 'count')    

    bow1['freq'] = bow1['count']/np.sum(bow1['count'])
    bow2['freq'] = bow2['count']/np.sum(bow2['count'])    
    merged = pd.merge(bow1, bow2, on='words')
    merged['divergence'] = merged['freq_x'] - merged['freq_y']
    merged = merged[['words', 'divergence']]

    return {
        'before': merged.sort_values(
            'divergence', ascending=False
        )['words'].head(topn).to_list(),
        'after': merged.sort_values(
            'divergence', ascending=True
        )['words'].head(topn).to_list()
    }
    

def word_density_plot(df, top_n=5):
    """
    Function on longer in use but leaving for EDA convenience
    """
    side1 = AFTER[:top_n]
    side2 = BEFORE[:top_n]
    
    found1 = pd.DataFrame(
        df[
            df['text'].str.contains(
                '|'.join(side1), case=False
            )
        ].groupby('Year')['Abstract'].count()
    )
    found2 = pd.DataFrame(
        df[
            df['text'].str.contains(
                '|'.join(side2), case=False
            )
        ].groupby('Year')['Abstract'].count()
    )
    counts = pd.DataFrame(
        df.groupby('Year')['Abstract'].count()
    )
    merged = found1.merge(counts, on='Year')
    merged.columns = ('abstract_count_1', 'abstract_count_all')
    merged = merged.merge(found2, on='Year')
    merged.columns = ('abstract_count_1', 'abstract_count_all', 'abstract_count_2')
    final = pd.DataFrame({
        'post-trump': merged['abstract_count_1']/merged['abstract_count_all'] * 100,
        'pre-trump': merged['abstract_count_2']/merged['abstract_count_all'] * 100,        
    })
    return final


def make_figure(
        dftotal,
        before_years,
        after_years,
        topn=9,
        destination=None
):
    fig = plt.figure(figsize=(32, 24))
    gs = gridspec.GridSpec(2, 2, width_ratios=[8,1])
    axes = [
        fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[:, 1]),
    ]
    
    bow1 = dftotal[dftotal['Year'].isin(before_years)]
    bow2 = dftotal[dftotal['Year'].isin(after_years)]

    fullbow = ' '.join(dftotal['text'] + dftotal['text'])
    top_bigrams_list = top_bigrams(
        fullbow,
        top_n_bigrams=400,
        min_freq=100,
    )
    bow1 = pd.DataFrame({
        'words': clean_text_with_bigrams(
            ' '.join(bow1['text']),
            top_bigrams_list=top_bigrams_list
        )
    })
    bow2 = pd.DataFrame({
        'words': clean_text_with_bigrams(
            ' '.join(bow2['text']),
            top_bigrams_list=top_bigrams_list
        )
    }) 

    bow1 = bow1.groupby('words').size().reset_index()
    bow1.columns = ('words', 'count')
    bow2 = bow2.groupby('words').size().reset_index()
    bow2.columns = ('words', 'count')    

    bow1['freq'] = bow1['count']/np.sum(bow1['count'])
    bow2['freq'] = bow2['count']/np.sum(bow2['count'])    
    merged = pd.merge(bow1, bow2, on='words')
    merged['divergence'] = merged['freq_x'] - merged['freq_y']
    merged = merged[['words', 'divergence']]
    
    before = merged.sort_values('divergence', ascending=False)[
        ['words', 'divergence']
    ].head(topn)
    after = merged.sort_values('divergence', ascending=True)[
        ['words', 'divergence']
    ].head(topn)
    barplotdf = pd.concat((before, after))
    barplotdf.columns = ('word', 'divergence')
    barplotdf = barplotdf.reindex(
        barplotdf["divergence"].abs().sort_values(ascending=False).index
    )
    colors = barplotdf["divergence"].apply(
        lambda x: after_color if x > 0 else before_color
    )
    
    barplotdf["divergence"] = barplotdf["divergence"] * 100
    
    axes[2].barh(barplotdf["word"], barplotdf["divergence"], color=colors)
    axes[2].axvline(0, color="black", linewidth=1)
    axes[2].set_title("ΔFrequency x 100")
    axes[2].invert_yaxis()    
    
    
    before = merged.sort_values(
        'divergence', ascending=False
    )['words'].head(topn).to_list()
    after = merged.sort_values(
        'divergence', ascending=True
    )['words'].head(topn).to_list()

    #--------#
    
    counts = dftotal.copy()[['text', 'Year']]
    counts['has_before'] = dftotal['text'].str.contains(
        '|'.join(before), case=False
    ).astype(bool)
    counts['has_after'] = dftotal['text'].str.contains(
        '|'.join(after), case=False
    ).astype(bool)
    
    found1 = pd.DataFrame(
        dftotal[
            dftotal['text'].str.contains(
                '|'.join(before), case=False
            )
        ].groupby('Year')['Abstract'].count()
    )
    found2 = pd.DataFrame(
        dftotal[
            dftotal['text'].str.contains(
                '|'.join(after), case=False
            )
        ].groupby('Year')['Abstract'].count()
    )
    total = pd.DataFrame(
        dftotal.groupby('Year')['Abstract'].count()
    )
    merged = found1.merge(total, on='Year')
    merged.columns = ('abstract_count_1', 'abstract_count_all')
    merged = merged.merge(found2, on='Year')
    merged.columns = ('abstract_count_1', 'abstract_count_all', 'abstract_count_2')
    merged = merged.reset_index()
    final = pd.DataFrame({
        'post-trump': merged['abstract_count_1']/merged['abstract_count_all'] * 100,
        'pre-trump': merged['abstract_count_2']/merged['abstract_count_all'] * 100,
        'year': merged['Year']
        #'top citations': merged_tc['Abstract_x']/merged_tc['Abstract_y'] * 100
    })
    
    axes[0].plot(
        final['year'], final['post-trump'],
        marker='o', linestyle='-',
        linewidth=1,
        markersize=7,
        color=after_color,     
    )
    axes[0].plot(
        final['year'], final['pre-trump'],
        marker='s',
        linestyle='--',
        linewidth=1,
        markersize=7,
        color=before_color,

    )
    axes[0].axvline(
        x=2016,
        color='black',
        linestyle='-',
        linewidth=1,
        alpha=0.8,
    )
    
    axes[0].set(xlabel = "Year")
    axes[0].set(ylabel="% of papers")
    axes[0].legend([
        f"Contains at least one of: {', '.join(before[:3])},...",
        f"Contains at least one of: {', '.join(after[:3])},...",        
    ])

    agg = counts.groupby('Year').apply(lambda x: pd.Series({
        f"Contains at least one of: {', '.join(before[:3])},..." : ((x['has_before']) & (~x['has_after'])).sum(),
        f"Contains at least one of: {', '.join(after[:3])},..." : ((x['has_after']) & (~x['has_before'])).sum(),
        "Contains at least one of each": (x['has_before'] & x['has_after']).sum()
    }))
    
    agg = agg.sort_index()    
    agg.plot(
        ax=axes[1], kind="area", stacked=True,
        alpha=0.8, figsize=(12,7),
        color=["#8CC084", "#DB9D47", "#593C8F"],
        linewidth=0,
    )
    agg['total'] = dftotal[
        ['Abstract', 'Year']
    ].groupby('Year')['Abstract'].size().sort_index()

    
    agg["total"].plot(ax=axes[1], color='#3E2A35', linewidth=2.5, linestyle="--", label="Total")
    
    axes[1].axvline(
        x=2016,
        color='black',
        linestyle='-',
        linewidth=1,
        alpha=0.8,
    )
    axes[1].set(xlabel = "Year")
    axes[1].set(ylabel="Number of papers")

    plt.suptitle(f"How 2016 changed misinfomation research", fontsize=18)    
    sns.despine()
    if destination is not None:
        plt.savefig(destination)
    plt.show()

def make_figure_wrapper(path_to_csv, destination):
    df = pd.read_csv(path_to_csv)
    df['text'] = df['Title'] + '. ' + df['Abstract']
    fig = make_figure(
        df,
        before_years,
        after_years,
        topn=9,
        destination=destination
    )

if __name__ == '__main__':
    make_figure_wrapper(
        'input/data.csv',
        'output/fig.pdf'
    )
    
