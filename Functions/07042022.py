# %%
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
from matplotlib import rcParams
from highlight_text import ax_text, fig_text
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

df = pd.read_csv("data/champions_goals_by_minute_07042022.csv", index_col = 0)


# %%

# ----------------------------------------------------------------
# The Visual

# Define a function to plot the bar charts.

def plot_barchart_minutes(ax, teamId, color, labels_x = False, labels_y = False):
    '''
    This function plots the bar chart showing the proportion
    of goals and xG created by each side in a specific interval of time.

    Args:
        ax (object): the matplotlib ax object
        teamId (int): the Fotmob team id
        color (str): the HEX color string to use for the plot
    '''

    global df

    data = df.copy()
    data = data[data["teamId"] == teamId].reset_index(drop = True)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    ax.grid(True, lw = 0.5, ls = ":", color = "lightgrey")

    ax.bar(
        data.index,
        data["xG_share"],
        color = color,
        alpha = 0.4,
        zorder = 3,
        width = .65
    )

    ax.bar(
        data.index,
        data["share"],
        color = color,
        width = 0.25,
        zorder =3
    )

    ax.set_xticks(data.index)
    if labels_x:
        ax.set_xticklabels([
            "First 15\nminutes",
            "15 - 30",
            "30 - 45",
            "45 - 60",
            "60 - 75",
            "Last 15\nminutes"
        ])
    else:
        ax.set_xticklabels([])

    ax.set_ylim(0,.5)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1%}"))

    if labels_y == False:
        ax.set_yticklabels([])

    # ---- Nice touches to the viz
    ax.plot([2.5, 2.5], [0, .5], color = "gray", lw = 1.15, ls = "--")

    for index, height in enumerate(data["share"]):
        text_ = ax.annotate(
            xy = (index, height),
            text = f"{height:.1%}",
            xytext = (0, 7.5),
            textcoords = "offset points",
            ha = "center",
            va = "center",
            size = 10,
            weight = "bold",
            color = "black"
        )
        text_.set_path_effects(
            [path_effects.Stroke(linewidth=1.75, foreground="white"), path_effects.Normal()]
        )

    return ax


# %%

colors = ['#206890', '#375196', '#69A8D8', '#302028', '#D8394C', '#085098',
       '#005898', '#a00028', '#005090', '#007838', '#0C2044', '#18B8E8']

for c in colors:

    fig = plt.figure(figsize=(6, 3), dpi = 100)
    ax = plt.subplot(111)



    plot_barchart_minutes(ax, 8342, c, True, False)

# %%

fig = plt.figure(figsize=(14, 14), dpi = 200)
nrows = 8
ncols = 3
gspec = gridspec.GridSpec(
    ncols=ncols, nrows=nrows, figure=fig, 
    height_ratios = [(1/nrows)*2. if x % 2 != 0 else (1/nrows)/2. for x in range(nrows)], hspace = 0.3
)

teams = [8456, 8633, 8564, 9823, 9847, 9773, 8593, 10013, 9925, 8342, 10243, 8391]

plot_counter = 0
logo_counter = 0
for row in range(nrows):
    for col in range(ncols):
        if row % 2 != 0:
            ax = plt.subplot(
                gspec[row, col],
                facecolor = "#EFE9E6"
            )

            teamId = teams[plot_counter]
            teamcolor = df[df["teamId"] == teamId]["teamColor"].iloc[0]

            if col == 0:
                labels_y = True
            else:
                labels_y = False
            
            if row == nrows - 1:
                labels_x = True
            else:
                labels_x = False
            
            plot_barchart_minutes(ax, teamId, teamcolor, labels_x, labels_y)           

            plot_counter += 1
        
        else:

            teamId = teams[logo_counter]
            teamName = df[df["teamId"] == teamId]["teamName"].iloc[0]

            goals_1h = df[df["teamId"] == teamId]["goals"].iloc[:3].sum()/df[df["teamId"] == teamId]["total_goals"].iloc[0]
            goals_2h = df[df["teamId"] == teamId]["goals"].iloc[3:].sum()/df[df["teamId"] == teamId]["total_goals"].iloc[0]

            fotmob_url = "https://images.fotmob.com/image_resources/logo/teamlogo/"
            logo_ax = plt.subplot(
                gspec[row,col],
                anchor = "NW", facecolor = "#EFE9E6"
            )
            club_icon = Image.open(urllib.request.urlopen(f"{fotmob_url}{teamId:.0f}.png")).convert("LA")
            logo_ax.imshow(club_icon)
            logo_ax.axis("off")

            # # Add the team name
            ax_text(
                x = 1.1, 
                y = 0.76,
                s = f"{teamName}",
                ax = logo_ax, 
                weight = "bold", 
                font = "Karla", 
                ha = "left", 
                size = 13, 
                annotationbbox_kw = {"xycoords":"axes fraction"}
            )

            # # Add the subtitles for each side
            ax_text(
                x = 1.1,
                y = 0.18,
                s = f"Goals 1H: {goals_1h:.1%} | Goals 2H: {goals_2h:.1%}",
                ax = logo_ax, 
                weight = "normal", 
                font = "Karla", 
                ha = "left", 
                size = 10, 
                annotationbbox_kw = {"xycoords":"axes fraction"}
            )

            logo_counter += 1


fig_text(
    x = 0.11, y = .94, 
    s = "When do Champions Score?",
    va = "bottom", ha = "left",
    fontsize = 25, color = "black", font = "DM Sans", weight = "bold"
)
fig_text(
	x = 0.11, y = .90, 
    s = "Percentage of xG and goals generated at each time interval during the match | Season 2021/2022 | viz by @sonofacorner\n<Dark areas and lables> denote the percentage of goals scored, whereas light areas denote xG.",
    highlight_textprops=[{"weight": "bold", "color": "black"}],
	va = "bottom", ha = "left",
	fontsize = 13, color = "#4E616C", font = "Karla"
)


plt.savefig(
	"figures/07042022_champions_score.png",
	dpi = 500,
	facecolor = "#EFE9E6",
	bbox_inches="tight",
    edgecolor="none",
	transparent = False
)

plt.savefig(
	"figures/07042022_champions_score_tr.png",
	dpi = 500,
	facecolor = "none",
	bbox_inches="tight",
    edgecolor="none",
	transparent = True
)