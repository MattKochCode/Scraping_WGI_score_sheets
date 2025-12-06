
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/matthew/Desktop/Unstructured_Data_Analytics/Scraping_WGI_score_sheets/WGI_2025_scores.csv")

open_df = df[df["class"].str.contains("Open", case=False, na=False)]

ind_open = open_df[open_df["class"].str.contains("Independent", case=False, na=False)]
sch_open = open_df[open_df["class"].str.contains("Scholastic", case=False, na=False)]

top_ind_open = ind_open.sort_values("total", ascending=False).head(10)
top_sch_open = sch_open.sort_values("total", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_ind_open["group"], top_ind_open["total"])
plt.xlabel("Total Score")
plt.title("Top Independent Open Class Groups (WGI 2025)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.barh(top_sch_open["group"], top_sch_open["total"])
plt.xlabel("Total Score")
plt.title("Top Scholastic Open Class Groups (WGI 2025)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
