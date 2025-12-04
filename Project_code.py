import pandas as pd
import requests
from io import StringIO
from bs4 import BeautifulSoup
import re

get_req = requests.get("https://recaps.competitionsuite.com/d821a435-4d55-4166-a41a-64b72a951aa6.htm")
comp_soup = BeautifulSoup(get_req.content)

comp_text = get_req.text

test = re.sub(r"(?<=content rank\'>)(\d+)", r'(\1)', comp_text)

tables = pd.read_html(StringIO(test), match="Effect")
len(tables)
tables[0]
tables[1]
tables[2]
tables[3]

'''
1. utilizing table  [1] try to lable the columns properly. Possibly labling as follows:
   'Music effect 1: Ovr', 'Music effect 1:Mus', 'Music effect 1: Total' 'Music effect 2: Ovr', 'Music effect 2: Mus', 'Music effect 2: Total' 
2. utilizing table  [1] try to create a dataframe that splits the overall score from the rank.

'''


master_col = [
    "group", "location",
    "effect_music_1_ovr","effect_music_1_mus","effect_music_1_tot",
    "effect_music_2_ovr","effect_music_2_mus","effect_music_2_tot",
    "effect_music_total",
    "effect_visual_1_ovr","effect_visual_1_vis","effect_visual_1_tot",
    "effect_visual_2_ovr","effect_visual_2_vis","effect_visual_2_tot",
    "effect_visual_total",
    "music_1_comp","music_1_perf","music_1_tot",
    "music_2_comp","music_2_perf","music_2_tot",
    "music_total",
    "visual_1_comp","visual_1_perf","visual_1_tot",
    "visual_2_comp","visual_2_perf","visual_2_tot",
    "visual_total",
    "sub_total","penalties","total"
]


test = tables[1]
df = test.iloc[3:].reset_index(drop=True)
df.columns = master_col


getnew_req = requests.get("https://recaps.competitionsuite.com/11afd1c8-276a-4052-bc54-4bd0cbd539ba.htm")
newcomp_soup = BeautifulSoup(getnew_req.content)

newcomp_text = getnew_req.text

newtest = re.sub(r"(?<=content rank\'>)(\d+)", r'(\1)', newcomp_text)

small_tables = pd.read_html(StringIO(newtest), match="Effect")
len(small_tables)


smalltest = small_tables[13]
smalldf = smalltest.iloc[3:].reset_index(drop=True)
small_cols = [
    "group", "location",
    "effect_music_1_ovr","effect_music_1_mus","effect_music_1_tot",
    "effect_visual_1_ovr","effect_visual_1_vis","effect_visual_1_tot",
    "music_1_comp","music_1_perf","music_1_tot",
    "visual_1_comp","visual_1_perf","visual_1_tot",
    "sub_total","penalties","total"
]

smalldf.columns = small_cols

small_df_full = smalldf.reindex(columns=master_col)


scores_df = df.copy()
ranks_df = df.copy()

for col in df.columns:

    # Only process string/object columns (skip numeric or metadata if they convert later)
    if df[col].dtype == object:

        # --- SCORE: everything before '(' ---
        scores_df[col] = (
            df[col]
            .str.extract(r'^([\d.]+)', expand=False)
            .astype(float)
        )

        # --- RANK: digits inside '( )' ---
        ranks_df[col] = (
            df[col]
            .str.extract(r'\((\d+)\)', expand=False)
            .astype(float)
        )

scores_df.head()
ranks_df.head()








# ===============================================================
# 1. Imports
# ===============================================================
import pandas as pd
import requests
from io import StringIO
from bs4 import BeautifulSoup
import re


# ===============================================================
# 2. MASTER COLUMN SCHEMA (now includes judge columns)
# ===============================================================
master_col = [

    "group", "location",

    # Effect Music judges + scores
    "effect_music_1_judge",
    "effect_music_1_ovr","effect_music_1_mus","effect_music_1_tot",
    "effect_music_2_judge",
    "effect_music_2_ovr","effect_music_2_mus","effect_music_2_tot",
    "effect_music_total",

    # Effect Visual judges + scores
    "effect_visual_1_judge",
    "effect_visual_1_ovr","effect_visual_1_vis","effect_visual_1_tot",
    "effect_visual_2_judge",
    "effect_visual_2_ovr","effect_visual_2_vis","effect_visual_2_tot",
    "effect_visual_total",

    # Music judges + scores
    "music_1_judge",
    "music_1_comp","music_1_perf","music_1_tot",
    "music_2_judge",
    "music_2_comp","music_2_perf","music_2_tot",
    "music_total",

    # Visual judges + scores
    "visual_1_judge",
    "visual_1_comp","visual_1_perf","visual_1_tot",
    "visual_2_judge",
    "visual_2_comp","visual_2_perf","visual_2_tot",
    "visual_total",

    # Summary columns
    "sub_total","penalties","total"
]


# ===============================================================
# 3. PROCESS LARGE TABLE (TWO-JUDGE PANELS)
# ===============================================================

# ---- 3A. Request & clean HTML ----
url_large = "https://recaps.competitionsuite.com/d821a435-4d55-4166-a41a-64b72a951aa6.htm"
req_large = requests.get(url_large)

html_large = req_large.text
html_large = re.sub(r"(?<=content rank\'>)(\d+)", r'(\1)', html_large)

tables_large = pd.read_html(StringIO(html_large), match="Effect")

# ---- 3B. Extract big scoring table ----
big_raw = tables_large[1]

# Header rows for judge extraction
header0 = big_raw.iloc[0]
header1 = big_raw.iloc[1]   # JUDGE NAMES
header2 = big_raw.iloc[2]

# ---- 3C. Remove header rows & assign score columns ----
big_df = big_raw.iloc[3:].reset_index(drop=True)

big_df.columns = [
    "group", "location",

    # Effect Music (judge 1 + judge 2)
    "effect_music_1_ovr","effect_music_1_mus","effect_music_1_tot",
    "effect_music_2_ovr","effect_music_2_mus","effect_music_2_tot",
    "effect_music_total",

    # Effect Visual (judge 1 + judge 2)
    "effect_visual_1_ovr","effect_visual_1_vis","effect_visual_1_tot",
    "effect_visual_2_ovr","effect_visual_2_vis","effect_visual_2_tot",
    "effect_visual_total",

    # Music
    "music_1_comp","music_1_perf","music_1_tot",
    "music_2_comp","music_2_perf","music_2_tot",
    "music_total",

    # Visual
    "visual_1_comp","visual_1_perf","visual_1_tot",
    "visual_2_comp","visual_2_perf","visual_2_tot",
    "visual_total",

    # Summary
    "sub_total","penalties","total"
]

# ---- 3D. Insert judge-name columns ----
big_df["effect_music_1_judge"]  = header1[2]
big_df["effect_music_2_judge"]  = header1[5]
big_df["effect_visual_1_judge"] = header1[9]
big_df["effect_visual_2_judge"] = header1[12]
big_df["music_1_judge"]         = header1[16]
big_df["music_2_judge"]         = header1[19]
big_df["visual_1_judge"]        = header1[23]
big_df["visual_2_judge"]        = header1[26]

# ---- 3E. Reorder columns to match master schema ----
big_df = big_df.reindex(columns=master_col)


# ===============================================================
# 4. PROCESS SMALL TABLE (ONE-JUDGE PANELS)
# ===============================================================

url_small = "https://recaps.competitionsuite.com/11afd1c8-276a-4052-bc54-4bd0cbd539ba.htm"
req_small = requests.get(url_small)

html_small = req_small.text
html_small = re.sub(r"(?<=content rank\'>)(\d+)", r'(\1)', html_small)

tables_small = pd.read_html(StringIO(html_small), match="Effect")

small_raw = tables_small[13]

# Extract header rows (judge names)
small_header1 = small_raw.iloc[1]

# ---- 4B. Drop header rows ----
small_df = small_raw.iloc[3:].reset_index(drop=True)

# ---- 4C. Assign score columns for one-judge tables ----
small_df.columns = [
    "group", "location",

    "effect_music_1_ovr","effect_music_1_mus","effect_music_1_tot",
    "effect_visual_1_ovr","effect_visual_1_vis","effect_visual_1_tot",
    "music_1_comp","music_1_perf","music_1_tot",
    "visual_1_comp","visual_1_perf","visual_1_tot",
    "sub_total","penalties","total"
]

# ---- 4D. Add judge columns (judge 2 = None for single-panel shows) ----
small_df["effect_music_1_judge"]  = small_header1[2]
small_df["effect_visual_1_judge"] = small_header1[5]
small_df["music_1_judge"]         = small_header1[8]
small_df["visual_1_judge"]        = small_header1[11]

small_df["effect_music_2_judge"]  = None
small_df["effect_visual_2_judge"] = None
small_df["music_2_judge"]         = None
small_df["visual_2_judge"]        = None

# ---- 4E. Expand into full schema ----
small_df_full = small_df.reindex(columns=master_col)


# ===============================================================
# 5. SPLIT SCORES & RANKS (inline, no functions)
# ===============================================================

# ---- 5A. Big table ----
big_scores = big_df.copy()
big_ranks  = big_df.copy()

for col in big_df.columns:
    if big_df[col].dtype == object:

        big_scores[col] = (
            big_df[col]
            .str.extract(r'^([\d.]+)', expand=False)
            .astype(float)
        )

        big_ranks[col] = (
            big_df[col]
            .str.extract(r'\((\d+)\)', expand=False)
            .astype(float)
        )

# ---- 5B. Small table ----
small_scores = small_df_full.copy()
small_ranks  = small_df_full.copy()

for col in small_df_full.columns:
    if small_df_full[col].dtype == object:

        small_scores[col] = (
            small_df_full[col]
            .str.extract(r'^([\d.]+)', expand=False)
            .astype(float)
        )

        small_ranks[col] = (
            small_df_full[col]
            .str.extract(r'\((\d+)\)', expand=False)
            .astype(float)
        )
