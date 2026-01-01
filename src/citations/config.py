TOP_N = 2
MIN_COMMUNITY_PAPERS = 10
dest = 'output/citations.png'

# --- making citation flow table -- #
table_data = (6075, 2350, 426, 1277, )#5282)
table_rows = [
    (1, 3, 5, 8, 10, 13,),
    (1,),
    (0,),
    (0,),
#    (0,),
]
# ---------- #

# --------------- paper ----------- #

background_color = '#FFFFFF'
before_color = "#8CC084"
after_color = "#DB9D47"
text_color = 'black'
color_map_colors = [
    background_color,
#    "#DB9D47", # gold         
#    "#8CC084", # green
    "#593C8F" # purple
]

# # ------------ presentation ---------#

# text_color = 'white'
# background_color = '#0F1219'
# before_color = '#FFFFFF'
# after_color = "#D33F49"
# color_map_colors = [
#     background_color,
#     "#D33F49",
# ]
