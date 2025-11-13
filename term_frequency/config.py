from nltk.corpus import stopwords
stop = stopwords.words('english')
stop.extend((
    'elsevier', 'rights', 'reserved', 'mesh', 'taylor', 'francis', 'copyright', 'llc', 'bt', 'lftb', 'springer', 'ieee', 'information', 'misinformation'
))
stop = [w.lower() for w in stop]

before_color = '#DB9D47'
after_color = "#8CC084"
before_years = [2011, 2012, 2013, 2014, 2015]
after_years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
