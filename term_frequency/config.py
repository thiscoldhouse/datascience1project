from nltk.corpus import stopwords
stop = stopwords.words('english')
stop.extend((
    'elsevier', 'rights', 'reserved', 'mesh', 'taylor', 'francis', 'copyright', 'llc', 'bt', 'lftb', 'springer', 'ieee', 'information', 'misinformation'
))
stop = [w.lower() for w in stop]

before_years = [2011, 2012, 2013, 2014, 2015]
after_years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
destination = 'output/fig.pdf'

# --------------- paper ----------- #

background_color = '#FFFFFF'
before_color = '#DB9D47'
after_color = "#8CC084"
text_color = 'black'
agg_plot_colors = [
    "#8CC084", # green
    "#DB9D47", # gold 
    "#593C8F" # purple
]

# ------------ presentation ---------#

text_color = 'white'
background_color = '#0F1219'
before_color = '#FFFFFF'
after_color = "#D33F49"
agg_plot_colors = [
    "#D33F49",
    '#FFFFFF',
    "#648381",
]
