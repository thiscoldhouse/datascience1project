import pandas as pd
import matplotlib.pyplot as plt

text_color = 'white'
background_color = '#0F1219'
before_color = '#FFFFFF'
after_color = "#D33F49"

df = pd.read_csv('input/misinformation.csv')

fig, ax = plt.subplots(
    figsize=(12,8),
    facecolor=background_color
)

df['freq_rolling'] = df['freq'].rolling(window=30).mean()
df['date'] = pd.to_datetime(df['date'])
df[['date', 'freq_rolling']].plot(
    ax=ax,
    color=text_color,
    x='date',
    y='freq_rolling',
    legend=False
)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_facecolor(background_color)
ax.tick_params(colors=text_color)
ax.xaxis.label.set_color(text_color)
ax.yaxis.label.set_color(text_color)
ax.axvline(
    pd.Timestamp('2016-01-01'),
    linestyle=':',
    linewidth=1,
    color=after_color,
)
ax.axvline(
    pd.Timestamp('2020-01-01'),
    linestyle=':',
    linewidth=1,
    color=after_color,
)

for spine in ax.spines.values():
    spine.set_color(text_color)

ax.set_title(
    "Frequency of Misinformation on Twitter c/o StoryWrangler",
    color=text_color
)
ax.set_xlabel(
    'Date'
)
ax.set_ylabel('Frequency (30 day rolling average)')
plt.xticks(rotation=45)
plt.savefig('output/storywrangler.pdf')
