import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size': 15})

# --- config --- #

# presentation
text_color = 'white'
background_color = '#0F1219'
before_color = '#FFFFFF'
after_color = "#D33F49"

# paper
background_color = '#FFFFFF'
before_color = '#DB9D47'
after_color = "#8CC084"
text_color = 'black'

# --- end config --- #

df = pd.read_csv('input/misinformation.csv')
fig, ax = plt.subplots(
    figsize=(8, 6),
    facecolor=background_color
)

df['Frequency'] = df['freq'].rolling(window=30).mean()
df['date'] = pd.to_datetime(df['date'])
df[['date', 'Frequency']].plot(
    ax=ax,
    color=text_color,
    x='date',
    y='Frequency',
    ylabel="Frequency",
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
    pd.Timestamp('2016-11-08'),
    linestyle=':',
    linewidth=1,
    color=before_color,
    label="November 8, 2016"
)

for spine in ax.spines.values():
    spine.set_color(text_color)

ax.set_title(
    "Frequency of \"Misinformation\" on Twitter",
    color=text_color
)
ax.set_xlabel(
    'Date'
)
ax.set_ylabel('Frequency (30 day rolling average)')
ax.legend()
plt.xticks(rotation=45)
plt.savefig('output/storywrangler.pdf')
