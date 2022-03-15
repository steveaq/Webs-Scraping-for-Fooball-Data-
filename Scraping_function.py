import requests
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import numpy as np
from math import pi
import os
from math import pi
from urllib.request import urlopen
import matplotlib.patheffects as pe
from highlight_text import fig_text
from adjustText import adjust_text






def get_player_data(x):
    warnings.filterwarnings("ignore")
    url = x
    page =requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = [element.text for element in soup.find_all("span")]
    name = name[7]
    metric_names = []
    metric_values = []
    remove_content = ["'", "[", "]", ","]
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        first_column = row.findAll('th')[0].contents
        metric_names.append(first_column)
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        first_column = row.findAll('td')[0].contents
        metric_values.append(first_column)

    metric_names = [item for sublist in metric_names for item in sublist]
    metric_values = [item for sublist in metric_values for item in sublist]
    df_player = pd.DataFrame()
    df_player['Name'] = name[0]
    for item in metric_names:
        df_player[item] = []

    name = name
    non_penalty_goals = (metric_values[0])
    npx_g = metric_values[1]
    shots_total = metric_values[2]
    assists = metric_values[3]
    x_a = metric_values[4]
    npx_g_plus_x_a = metric_values[5] 
    shot_creating_actions = metric_values[6] 
    passes_attempted = metric_values[7] 
    pass_completion_percent = metric_values[8] 
    progressive_passes = metric_values[9] 
    progressive_carries = metric_values[10] 
    dribbles_completed = metric_values[11] 
    touches_att_pen = metric_values[12]
    progressive_passes_rec = metric_values[13] 
    pressures = metric_values[14] 
    tackles = metric_values[15] 
    interceptions = metric_values[16] 
    blocks = metric_values[17]
    clearances = metric_values[18]
    aerials_won = metric_values[19]
    df_player.loc[0] = [name, non_penalty_goals, npx_g, shots_total, assists, x_a, npx_g_plus_x_a, shot_creating_actions, passes_attempted, pass_completion_percent,
                        progressive_passes, progressive_carries, dribbles_completed, touches_att_pen, progressive_passes_rec, pressures, tackles, interceptions, blocks,
                        clearances, aerials_won] 
    return df_player

def get_player_multi_data(url_list:list):
    appended_data = []
    for url in url_list:
        warnings.filterwarnings("ignore")
        page =requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = [element.text for element in soup.find_all("span")]
        name = name[7]
        metric_names = []
        metric_values = []
        remove_content = ["'", "[", "]", ","]
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            first_column = row.findAll('th')[0].contents
            metric_names.append(first_column)
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            first_column = row.findAll('td')[0].contents
            metric_values.append(first_column)

        metric_names = [item for sublist in metric_names for item in sublist]
        metric_values = [item for sublist in metric_values for item in sublist]

        df_player = pd.DataFrame()
        df_player['Name'] = name[0]
        for item in metric_names:
            df_player[item] = []

        name = name
        non_penalty_goals = (metric_values[0])
        npx_g = metric_values[1]
        shots_total = metric_values[2]
        assists = metric_values[3]
        x_a = metric_values[4]
        npx_g_plus_x_a = metric_values[5] 
        shot_creating_actions = metric_values[6] 
        passes_attempted = metric_values[7] 
        pass_completion_percent = metric_values[8] 
        progressive_passes = metric_values[9] 
        progressive_carries = metric_values[10] 
        dribbles_completed = metric_values[11] 
        touches_att_pen = metric_values[12]
        progressive_passes_rec = metric_values[13] 
        pressures = metric_values[14] 
        tackles = metric_values[15] 
        interceptions = metric_values[16] 
        blocks = metric_values[17]
        clearances = metric_values[18]
        aerials_won = metric_values[19]
        df_player.loc[0] = [name, non_penalty_goals, npx_g, shots_total, assists, x_a, npx_g_plus_x_a, shot_creating_actions, passes_attempted, pass_completion_percent,
                            progressive_passes, progressive_carries, dribbles_completed, touches_att_pen, progressive_passes_rec, pressures, tackles, interceptions, blocks,
                            clearances, aerials_won]
        appended_data.append(df_player)
    appended_data = pd.concat(appended_data)
    return appended_data

def generate_player_comparison(url_list, view):
    df_player_comp = get_player_multi_data(url_list)

    def p2f(x):
        return float(x.strip('%'))/100

    df_player_comp["Pass Completion %"] = df_player_comp["Pass Completion %"].apply(p2f)

    df_player_comp[['Non-Penalty Goals', 'npxG', 'Shots Total', 'Assists', 'xA',
        'npxG+xA', 'Shot-Creating Actions', 'Passes Attempted',
        'Pass Completion %', 'Progressive Passes', 'Progressive Carries',
        'Dribbles Completed', 'Touches (Att Pen)', 'Progressive Passes Rec',
        'Pressures', 'Tackles', 'Interceptions', 'Blocks', 'Clearances',
        'Aerials won']] = df_player_comp[['Non-Penalty Goals', 'npxG', 'Shots Total', 'Assists', 'xA',
        'npxG+xA', 'Shot-Creating Actions', 'Passes Attempted',
        'Pass Completion %', 'Progressive Passes', 'Progressive Carries',
        'Dribbles Completed', 'Touches (Att Pen)', 'Progressive Passes Rec',
        'Pressures', 'Tackles', 'Interceptions', 'Blocks', 'Clearances',
        'Aerials won']].apply(pd.to_numeric)

    df_player_comp_attacking= df_player_comp[['Name','Non-Penalty Goals', 'npxG', 'Shots Total']]
    # 'xA','npxG+xA', 'Shot-Creating Actions'
    df_player_comp_playmaking= df_player_comp[['Name','Assists','Dribbles Completed',
         'Touches (Att Pen)', 'Progressive Passes Rec','Passes Attempted',
        'Pass Completion %', 'Progressive Passes', 'Progressive Carries']]
    df_player_comp_defensive= df_player_comp[['Name','Aerials won','Pressures', 'Tackles', 'Interceptions', 'Blocks']]
    if view == "attack":
        fig, ax =plt.subplots(1,3, figsize=(27,6))
        sb.barplot(df_player_comp_attacking['Name'], df_player_comp_attacking['Non-Penalty Goals'], ax=ax[0]).set(title='Non Penalty Goals')
        sb.barplot(df_player_comp_attacking['Name'], df_player_comp_attacking['npxG'], ax=ax[1]).set(title='Non Penalty xG')
        sb.barplot(df_player_comp_attacking['Name'], df_player_comp_attacking['Shots Total'], ax=ax[2]).set(title='Total Shots')
    elif view == "playmaking":
        fig, ax =plt.subplots(1,4, figsize=(27,6))
        sb.barplot(df_player_comp_playmaking['Name'], df_player_comp_playmaking['Assists'], ax=ax[0]).set(title='Assists')
        sb.barplot(df_player_comp_playmaking['Name'], df_player_comp_playmaking['Dribbles Completed'], ax=ax[1]).set(title='Dribbles Completed')
        sb.barplot(df_player_comp_playmaking['Name'], df_player_comp_playmaking['Touches (Att Pen)'], ax=ax[2]).set(title='Touches in Pen Area')
        sb.barplot(df_player_comp_playmaking['Name'], df_player_comp_playmaking['Progressive Passes Rec'], ax=ax[3]).set(title='Progressive Passes Received')
    elif view == "defensive":
        fig, ax =plt.subplots(1,5, figsize=(36,8))
        sb.barplot(df_player_comp_defensive['Name'], df_player_comp_defensive['Aerials won'], ax=ax[0]).set(title='Aerials Won')
        sb.barplot(df_player_comp_defensive['Name'], df_player_comp_defensive['Pressures'], ax=ax[1]).set(title='Pressures')
        sb.barplot(df_player_comp_defensive['Name'], df_player_comp_defensive['Tackles'], ax=ax[2]).set(title='Tackles')
        sb.barplot(df_player_comp_defensive['Name'], df_player_comp_defensive['Interceptions'], ax=ax[3]).set(title='Interceptions')
        sb.barplot(df_player_comp_defensive['Name'], df_player_comp_defensive['Blocks'], ax=ax[4]).set(title='Blocks')
    else: 
        print('Please check your spelling. options are: attack, playmaking or defensive')   


def compare_players_percentile(url_list):
    appended_data = []
    for x in url_list:

        warnings.filterwarnings("ignore")
        
        url = x
        page =requests.get(url)
        soup= BeautifulSoup(page.content, 'html.parser')
        name = [element.text for element in soup.find_all("span")]
        name = name[7]
        
        metric_names = []
        metric_values = []
        
        
        remove_content = ["'", "[", "]", ",", "%"]
        
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            first_column = row.findAll('th')[0].contents
            metric_names.append(first_column)
            
            
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            first_column = row.findAll('td')[1].contents
            metric_values.append(first_column)
            
            
        clean_left = []
        splitat_r = 65
        splitat_l = 67

        for item in metric_values:
            item = str(item).strip('[]')
            left, right = item[:splitat_l], item[splitat_r:]
            clean_left.append(left)

        clean_overall= []
        
        for item in clean_left:
            item = str(item).strip('[]')
            left, right = item[:splitat_l], item[splitat_r:]
            clean_overall.append(right)
        
        clean = []
        
        for item in clean_overall:
            item = item.replace("<","")
            clean.append(item)
            
        metric_names  = [item for sublist in metric_names  for item in sublist]

        clean = list(filter(None, clean))

            
        df_player = pd.DataFrame()
        
        
        df_player['Name'] = name[0]
        for item in metric_names:
            df_player[item] = []


        name = name
        non_penalty_goals = (clean[0])
        npx_g = clean[1]
        shots_total = clean[2]
        assists = clean[3]
        x_a = clean[4]
        npx_g_plus_x_a = clean[5] 
        shot_creating_actions = clean[6] 
        passes_attempted = clean[7] 
        pass_completion_percent = clean[8] 
        progressive_passes = clean[9] 
        progressive_carries = clean[10] 
        dribbles_completed = clean[11] 
        touches_att_pen = clean[12]
        progressive_passes_rec = clean[13] 
        pressures = clean[14] 
        tackles = clean[15] 
        interceptions = clean[16] 
        blocks = clean[17]
        clearances = clean[18]
        aerials_won = clean[19]
        df_player.loc[0] = [name, non_penalty_goals, npx_g, shots_total, assists, x_a, npx_g_plus_x_a, shot_creating_actions, passes_attempted, pass_completion_percent,
                            progressive_passes, progressive_carries, dribbles_completed, touches_att_pen, progressive_passes_rec, pressures, tackles, interceptions, blocks,
                            clearances, aerials_won]
        appended_data.append(df_player)

    df_player_comp = pd.concat(appended_data)

    df_player_comp[['Non-Penalty Goals', 'npxG', 'Shots Total', 'Assists', 'xA',
            'npxG+xA', 'Shot-Creating Actions', 'Passes Attempted',
            'Pass Completion %', 'Progressive Passes', 'Progressive Carries',
            'Dribbles Completed', 'Touches (Att Pen)', 'Progressive Passes Rec',
            'Pressures', 'Tackles', 'Interceptions', 'Blocks', 'Clearances',
            'Aerials won']] = df_player_comp[['Non-Penalty Goals', 'npxG', 'Shots Total', 'Assists', 'xA',
            'npxG+xA', 'Shot-Creating Actions', 'Passes Attempted',
            'Pass Completion %', 'Progressive Passes', 'Progressive Carries',
            'Dribbles Completed', 'Touches (Att Pen)', 'Progressive Passes Rec',
            'Pressures', 'Tackles', 'Interceptions', 'Blocks', 'Clearances',
            'Aerials won']].apply(pd.to_numeric)
        
    categories = ['Non-Penalty Goals', 'npxG', 'Shots Total', 'Assists', 'xA',
        'npxG+xA', 'Shot-Creating Actions', 'Passes Attempted',
        'Pass Completion %', 'Progressive Passes', 'Progressive Carries',
        'Dribbles Completed', 'Touches (Att Pen)', 'Progressive Passes Rec',
        'Pressures', 'Tackles', 'Interceptions', 'Blocks', 'Clearances',
        'Aerials won']



    df_player_plot_1 = df_player_comp.reset_index(drop=True)

    df_player_plot_1 = df_player_plot_1.iloc[0].values.tolist()
    player_1_name = df_player_plot_1[0]
    del df_player_plot_1[0]

    df_player_plot_2 = df_player_comp.reset_index(drop=True)
    df_player_plot_2 = df_player_plot_2.iloc[1].values.tolist()
    player_2_name = df_player_plot_2[0]
    del df_player_plot_2[0]

    df_player_1_plot = df_player_plot_1

    df_player_2_plot = df_player_plot_2

    df_player_1_plot_numeric = []
        
    for item in df_player_1_plot:
        item = int(item)
        df_player_1_plot_numeric.append(item)
        
    df_player_2_plot_numeric = []

    for item in df_player_2_plot:
        item = int(item)
        df_player_2_plot_numeric.append(item)    

    N = 20

    angles = [n / float(N) * 2 * pi for n in range(N)]

    plt.figure(figsize=(40,10))

    ax = plt.subplot(111, polar=True)

    ax.set_theta_offset(pi / 2)

    ax.set_theta_direction(-1)

    plt.xticks(angles[:], categories)

    a = df_player_1_plot_numeric
    b = df_player_2_plot_numeric

    ax.plot(angles, a, linewidth=1, linestyle='solid', label=player_1_name, color ='blue')
    ax.fill(angles, a, 'b', alpha=0.3, color ='blue')

    ax.plot(angles, b, linewidth=1, linestyle='solid', label=player_2_name, color ='green')
    ax.fill(angles, b, 'b', alpha=0.3, color ='green')
        
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

def generate_squadlist(url):
    # name = [element.text for element in BeautifulSoup.find_all("span")]
    # name = name[7]    
    html = requests.get(url).text
    data = BeautifulSoup(html, 'html5')
    table = data.find('table')
    cols = []

    for header in table.find_all('th'):
        cols.append(header.string)

    columns = cols[8:37] #gets necessary column headers
    players = cols[37:-2]

    #display(columns)
    rows = [] #initliaze list to store all rows of data
    for rownum, row in enumerate(table.find_all('tr')): #find all rows in table
        if len(row.find_all('td')) > 0: 
            rowdata = [] #initiliaze list of row data
            for i in range(0,len(row.find_all('td'))): #get all column values for row
                rowdata.append(row.find_all('td')[i].text)
            rows.append(rowdata)
    df = pd.DataFrame(rows, columns=columns)

    df.drop(df.tail(2).index,inplace=True)
    df["Player"] = players
    df.drop('Matches', axis=1, inplace=True)
    df['Nation'] = df['Nation'].str[3:]
    # df["team"] = name
    df.set_index("Player")

    return df 

# # team = "https://fbref.com/en/squads/d48ad4ff/Napoli-Stats"
# team_name = team[37:-6]
# squad_stats_per_team = generate_squadlist(team)
# squad_stats_per_team

def years_converter(variable_value):
    years = variable_value[:-4]
    days = variable_value[3:]
    years_value = pd.to_numeric(years)
    days_value = pd.to_numeric(days)
    day_conv = days_value/365
    final_val = years_value + day_conv

    return final_val

# squad_stats_per_team['age_new'] = squad_stats_per_team.apply(lambda x: years_converter(x['Age']), axis=1)

def squad_age_profile_chart(df, team_name):
        df[["90s"]] = df[["90s"]].apply(pd.to_numeric)        
        df["Min_pct"] = 100*df["90s"]/38 ##number of matches in a Serie A season
        df = df.dropna(subset=["Age", "Min_pct"])
        df = df.loc[:len(df)-1, :]
        df[["Player", "Pos", "age_new", "Min_pct"]].head()

        line_color = "silver"
        marker_color = "dodgerblue"
        fig, ax = plt.subplots(figsize=(12, 8)) 

        ax.scatter(df["age_new"], df["Min_pct"],alpha=0.8) ##scatter points
        ax.fill([24, 29, 29, 24], [-6, -6, 106, 106], color='limegreen',
                alpha=0.3, zorder=2) ##the peak age shaded region
        ax.text(26.5, 55, "PEAK", color=line_color, zorder=3, 
                alpha=2, fontsize=26, rotation=90, ha='center',
                va='center', fontweight='bold') ## `PEAK` age text
        texts = [] ##plot player names
        for row in df.itertuples():
                texts.append(ax.text(row.age_new, row.Min_pct, row.Player, fontsize=8, ha='center', va='center', zorder=10))
                adjust_text(texts) ## to remove overlaps between labels

        ## update plot
                ax.set(xlabel="Age", ylabel="Share of Minutes Played %", ylim=(-5, 105), xlim=(16, 40)) ## set labels and limits

        ##grids and spines
        ax.grid(color=line_color, linestyle='--', linewidth=0.8, alpha=0.5)   
        for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)
                ax.spines[spine].set_color(line_color)
        # ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.xaxis.set_ticks(range(16, 44, 4)) ##fix the tick frequency 
        ax.xaxis.label.set(fontsize=12, fontweight='bold')
        ax.yaxis.label.set(fontsize=12, fontweight='bold') ## increase the weight of the axis labels

        ax.set_position([0.08, 0.08, 0.82, 0.78]) ## make space for the title on top of the axes

        ## title and subtitle
        fig.text(x=0.08, y=0.92, s=f"{team_name} | Squad Age Profile", 
                ha='left', fontsize=20, fontweight='book', 
                path_effects=[pe.Stroke(linewidth=3, foreground='0.15'),
                        pe.Normal()]) 
        fig.text(x=0.08, y=0.88, s=f"Serie A | 2020-21", ha='left', 
                fontsize=20, fontweight='book', 
                path_effects=[pe.Stroke(linewidth=3, foreground='0.15'),
                        pe.Normal()])

def team_fixture_data(x):
    url = x
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    count = 0 
    table = soup.find("tbody")

    pre_df = dict()
    features_wanted =  {"date" , "time","comp","Round","dayofweek", "venue","result","goals_for","goals_against","opponent","xg_for","xg_against","possession","attendance","captain", "formation","referee"} #add more features here!!
    rows = table.find_all('tr')
    for row in rows:
        for f in features_wanted:
            if (row.find('th', {"scope":"row"}) != None) & (row.find("td",{"data-stat": f}) != None):
                cell = row.find("td",{"data-stat": f})
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if f in pre_df:
                    pre_df[f].append(text)
                else:
                    pre_df[f]=[text]
                
    df = pd.DataFrame.from_dict(pre_df)
    return df 

# league_results = team_fixture_data("https://fbref.com/en/squads/d48ad4ff/2021-2022/matchlogs/all_comps/schedule/Napoli-Scores-and-Fixtures-All-Competitions")
# league_results = league_results.loc[(league_results['captain'] != '') & (league_results['comp'] == 'Serie A')]
# league_results   
team_name = ""
def generate_xg_analysis_chart(df):
        window = 5
        gd_color = "green"
        xgd_color = "blue"

        df[["goals_for","xg_for","xg_against","goals_against"]] = df[["goals_for","xg_for","xg_against","goals_against"]].apply(pd.to_numeric)

        df["GD"] = df["goals_for"] - df["goals_against"]
        df["xGD"] = df["xg_for"] - df["xg_against"]

        gd_rolling = df["GD"].rolling(window).mean().values[window:]
        xgd_rolling = df["xGD"].rolling(window).mean().values[window:]

        plt.rcParams['font.family'] = 'Palatino Linotype' ##set global font
        fig, ax = plt.subplots(figsize=(12, 8))

        ax.plot(gd_rolling, color=gd_color,  linestyle="-.", marker="o",  mfc=gd_color, mec="white", markersize=8, mew=0.4, zorder=10)  ##goal-difference
        ax.plot(xgd_rolling, color=xgd_color,  linestyle="-.", marker = "o", mfc=xgd_color, mec="white", markersize=8, mew=0.4, zorder=10) ##expected goals difference

        ax.fill_between(x=range(len(gd_rolling)), y1=gd_rolling, y2=xgd_rolling, where = gd_rolling>xgd_rolling, 
                        alpha=0.2, color=gd_color, interpolate=True, zorder=5) ##shade the areas in between
        ax.fill_between(x=range(len(gd_rolling)), y1=gd_rolling, y2=xgd_rolling, where = gd_rolling<=xgd_rolling, 
                        alpha=0.2, color=xgd_color, interpolate=True, zorder=5)

        ax.grid(linestyle="dashed", lw=0.7, alpha=0.1, zorder=1) ## a faint grid
        for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)  
        ax.set_position([0.08, 0.08, 0.82, 0.78]) ## make space for the title on top of the axes

        ## labels, titles and subtitles
        ax.set(xlabel=f"{window} match rolling mean", xlim=(-1, len(df)-window))     
        ax.xaxis.label.set(fontsize=12, fontweight='bold')    

        fig.text(x=0.08, y=0.92, s=f"{team_name} | Performance Trend", 
                ha='left', fontsize=24, fontweight='book', 
                path_effects=[pe.Stroke(linewidth=3, foreground='0.15'),
                        pe.Normal()])   

        fig_text(x=0.08, y=0.90, ha='left',
                fontsize=18, fontweight='book',
                s='2020-21 | <Goal Difference> vs <Expected Goal Difference>',
                path_effects=[pe.Stroke(linewidth=3, foreground='0.15'),
                        pe.Normal()],
                highlight_textprops=[{"color": gd_color},
                                        {"color": xgd_color}])
        
#     fig.savefig("xg-trend-line-chart", dpi=180) ##save image

def generate_league_data(x):
    url = x
    page = urlopen(url).read()
    soup = BeautifulSoup(page)
    count = 0 
    table = soup.find("tbody")

    pre_df = dict()
    features_wanted =  {"squad" , "games","wins","draws","losses", "goals_for","goals_against", "points", "xg_for","xg_against","xg_diff","attendance","xg_diff_per90", "last_5"} #add more features here!!
    rows = table.find_all('tr')
    for row in rows:
        for f in features_wanted:
            if (row.find('th', {"scope":"row"}) != None) & (row.find("td",{"data-stat": f}) != None):
                cell = row.find("td",{"data-stat": f})
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if f in pre_df:
                    pre_df[f].append(text)
                else:
                    pre_df[f]=[text]
                
    df = pd.DataFrame.from_dict(pre_df)
    df["games"] = pd.to_numeric(df["games"])
    df["xg_diff_per90"] = pd.to_numeric(df["xg_diff_per90"])
    df["minutes_played"] = df["games"] *90
    return(df)

# df = generate_league_data("https://fbref.com/en/comps/9/Premier-League-Stats")
# df['path'] = df["squad"] + '.png'
# df[["squad","xg_for","xg_against", "path"]]

def p90_Calculator(variable_value, minutes_played):
    
    variable_value = pd.to_numeric(variable_value)
    
    ninety_minute_periods = minutes_played/90
    
    p90_value = variable_value/ninety_minute_periods
    
    return p90_value

def form_ppg_calc(variable_value):
    wins = variable_value.count("W")
    draws = variable_value.count("D")
    losses = variable_value.count("L")
    points = (wins*3) + (draws)
    ppg = points/5
    return ppg

def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.05, alpha = 1)

# df['xG_p90'] = df.apply(lambda x: p90_Calculator(x['xg_for'], x['minutes_played']), axis=1)
# df['xGA_p90'] = df.apply(lambda x: p90_Calculator(x['xg_against'], x['minutes_played']), axis=1)
# df['ppg_form'] = df.apply(lambda x: form_ppg_calc(x['last_5']), axis=1)
df = [[]]
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(df["ppg_form"], df["xg_diff_per90"])

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(os.path.join("team_logos/"+row["path"])), (row["ppg_form"], row["xg_diff_per90"]), frameon=False)
    ax.add_artist(ab)

# Set font and background colour
bgcol = '#fafafa'

# Create initial plot
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['ppg_form'], df['xg_diff_per90'], c=bgcol)

# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

# Change ticks
plt.tick_params(axis='x', labelsize=6, color='#ccc8c8')
plt.tick_params(axis='y', labelsize=6, color='#ccc8c8')

# Plot badges
def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.05, alpha = 1)

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(os.path.join("team_logos/"+row["path"])), (row['ppg_form'], row['xg_diff_per90']), frameon=False)
    ax.add_artist(ab)

# Add average lines
plt.hlines(df['xg_diff_per90'].mean(), df['ppg_form'].min(), df['ppg_form'].max(), color='#c2c1c0')
plt.vlines(df['ppg_form'].mean(), df['xg_diff_per90'].min(), df['xg_diff_per90'].max(), color='#c2c1c0')
ax.axvspan(2.0, 3,0, alpha=0.1, color='green',label= "In Form")
ax.axvspan(0.9, 1,2, alpha=0.1, color='yellow',label= "Mediorcre")
ax.axvspan(0.0, 0.5, alpha=0.1, color='red',label= "relegation on speed dail")

# Text

## Title & comment
fig.text(.15,.98,'Last 5 ppg vs xG Difference per 90',size=18)

## Avg line explanation
fig.text(.06,.14,'xG Difference per 90', size=9, color='#575654',rotation=90)
fig.text(.12,0.05,'Last 5 ppg', size=9, color='#575654')

## Axes titles
fig.text(.76,.535,'Avg. xG Difference per 90', size=6, color='#c2c1c0')
fig.text(.325,.17,'Avg. Last 5 ppg', size=6, color='#c2c1c0',rotation=90)

## Save plot
plt.savefig('xGChart.png', dpi=1200, bbox_inches = "tight")