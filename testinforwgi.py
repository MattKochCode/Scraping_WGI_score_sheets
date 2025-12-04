import pandas as pd

link = "https://recaps.competitionsuite.com/17800444-1293-42cb-84fb-5f56df0393fa.htm"

tables = pd.read_html(link)
tables[0].columns
tables[0]
tables[1]