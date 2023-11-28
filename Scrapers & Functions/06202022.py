#%%
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
from matplotlib import rcParams
import numpy as np
from highlight_text import fig_text
import pandas as pd

from PIL import Image
import urllib
import os

# --- Use this only if you have already downloaded fonts into your
# --- local directory.

# Add pretty fonts

font_path = r"" #Set the path to where the fonts are located

for x in os.listdir(font_path):
    for y in os.listdir(f"{font_path}/{x}"):
        if y.split(".")[-1] == "ttf":
            fm.fontManager.addfont(f"{font_path}/{x}/{y}")
            try:
                fm.FontProperties(weight=y.split("-")[-1].split(".")[0].lower(), fname=y)
            except Exception as e:
                print(f"Font {y} could not be added.")
                continue

rcParams['font.family'] = 'Karla'

# --- Reading the data

df = pd.read_csv("data/06202022_bundesliga.csv", index_col = 0)
df = (
        df
        .sort_values(by = ["variable", "value"], ascending = True)
        .reset_index(drop = True)
)


fig = plt.figure(figsize=(6.5, 10), dpi = 200, facecolor="#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")

# Adjust spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(True, color = "lightgrey", ls = ":")

# Define the series
teams = list(df["team_id"].unique())
Y = np.arange(len(teams))
X_xg = df[df["variable"] == "xG_ag"]["value"]
X_goals = df[df["variable"] == "score_ag"]["value"]

# Fix axes limits
ax.set_ylim(-.5, len(teams) - .5)
ax.set_xlim(
    min(X_goals.min(), X_xg.min(), 30), 
    max(X_goals.max(), X_xg.max(), 90)
)

# Scatter plots
ax.scatter(X_xg, Y, color = "#74959A", s = 150, alpha = 0.35, zorder = 3)
ax.scatter(X_goals, Y, color = "#495371", s = 150, alpha = 0.35, zorder = 3)
ax.scatter(X_xg, Y, color = "none", ec = "#74959A", s = 180, lw = 2.5, zorder = 3)
ax.scatter(X_goals, Y, color = "none", ec = "#495371", s = 180, lw = 2.5, zorder = 3)


# Add line chart between points and difference annotation
for index in Y:
    difference = X_xg.iloc[index] - X_goals.iloc[index]
    if difference > 0:
        color = "#74959A" 
        x_adj = -1.75
        anot_position = X_xg.iloc[index]
        anot_aux_sign = "-"
    else:
        color = "#495371"
        x_adj = 1.75
        anot_position = X_goals.iloc[index]
        anot_aux_sign = "+"
    
    ax.annotate(
        xy = (anot_position, index),
        text = f"{anot_aux_sign} {abs(difference):.1f}",
        xytext = (13, -2),
        textcoords = "offset points",
        size = 8,
        color = color,
        weight = "bold"
    )
    
    if abs(difference) < 3.5:
        continue
    ax.plot(
        [X_xg.iloc[index] + x_adj, X_goals.iloc[index] + x_adj*(-1)],
        [index, index],
        lw = 2.5,
        color = color,
        zorder = 2
    )

DC_to_FC = ax.transData.transform
FC_to_NFC = fig.transFigure.inverted().transform

# Native data to normalized data coordinates
DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

fotmob_url = "https://images.fotmob.com/image_resources/logo/teamlogo/"
for index, team_id in enumerate(teams):
    ax_coords = DC_to_NFC([25, index - 0.55])
    logo_ax = fig.add_axes([ax_coords[0], ax_coords[1], 0.045, 0.045], anchor = "C")
    club_icon = Image.open(urllib.request.urlopen(f"{fotmob_url}{team_id:.0f}.png")).convert("LA")
    logo_ax.imshow(club_icon)
    logo_ax.axis("off")


# Remove tick labels
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
false_ticks = ax.set_yticklabels([])

fig_text(
    x = 0.15, y = .9, 
    s = "During the 21/22 season almost every Bundesliga\nside <outperformed> their <xG conceded>",
    highlight_textprops = [
        {"color": "#495371"},
        {"color":"#74959A"}
    ],
    va = "bottom", ha = "left",
    fontsize = 14, color = "black", font = "DM Sans", weight = "bold"
)
fig_text(
	x = 0.15, y = .885, 
    s = "German Bundesliga | 2021 - 2022 season | viz by @sonofacorner",
	va = "bottom", ha = "left",
	fontsize = 8, color = "#4E616C", font = "Karla"
)

# # ---- The League's logo
league_icon = Image.open(urllib.request.urlopen(f"https://images.fotmob.com/image_resources/logo/leaguelogo/54.png"))
league_ax = fig.add_axes([0.055, 0.89, 0.065, 0.065], zorder=1)
league_ax.imshow(league_icon)
league_ax.axis("off")

plt.savefig(
	"figures/06202022_bundelsiga_xg.png",
	dpi = 500,
	facecolor = "#EFE9E6",
	bbox_inches="tight",
    edgecolor="none",
	transparent = False
)

plt.savefig(
	"figures/06202022_bundelsiga_xg_tr.png",
	dpi = 500,
	facecolor = "none",
	bbox_inches="tight",
    edgecolor="none",
	transparent = True
)
