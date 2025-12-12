
RESOLUTION = 1
TOP_N = 2
n_terms_for_table = 20
N_INITIAL_COMMUNITIES = 10
MIN_COMMUNITY_PAPERS = 10
tables_dests = (
    'output/tables0.tex',
    'output/tables1.tex'
)
graph_dests = (
    'output/communities-graph.pdf',
    'output/first-communities.pdf'
)

from nltk.corpus import stopwords
stop = stopwords.words('english')
stop.extend((
    'elsevier', 'rights', 'reserved', 'mesh', 'taylor', 'francis', 'copyright', 'llc', 'bt', 'lftb', 'springer', 'ieee', 'information', 'misinformation', 'claimscan', 
))
stop = [w.lower() for w in stop]

# Junk paper that appears duplicated 22 times.
delete_title = 'Medical misinformation: vet the message!'


# --------------- paper ----------- #

background_color = '#FFFFFF'
before_color = '#DB9D47'
after_color = "#8CC084"
text_color = 'black'

colors = [
    '#6A041D',
    '#593C8F',
    '#1B512D',
    '#DB9D47',
    '#8CC084',
    '#090446',
    '#666A86',
    '#E86A92',
    '#009DDC',
    '#FFDDD2',
    '#A72608',
    '#63D2FF',
    '#433A3F',
    '#28190E',
]



# # ------------ presentation ---------#

# text_color = 'white'
# background_color = '#0F1219'
# before_color = '#FFFFFF'
# after_color = "#D33F49"
# colors = [
#     "#D33F49",
#     '#FFFFFF',
#     "#648381",
#     "#FBAF00",
#     "#574F2A",
#     "#EC4E20",
#     "#00A9A5",
#     "#CED097",
#     "#C52184",
#     "#7C77B9",
#     "#9A348E",
#     "#50A2A7",
#     "#FFC4EB",
#     "#D58936",
#     "#C2CFB2"
# ]
