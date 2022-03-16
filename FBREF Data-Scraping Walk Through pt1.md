---
title: 'arXiv-GPT: predicting Machine Learning abstracts'
date: 28-09-2020
classes: wide
---

*Code & notebook for this post can be found [here](https://github.com/steveaq/Webs-Scraping-for-Fooball-Data-/blob/main/FBREF%20League%20%26%20Team%20Data%20Exploration.ipynb). 

In my previous post, which you can find [here](), I outlined the current data landscape in the football analytics world and how one might go about aquiring those related metrics.

This post is a part of series of posts, where we will explore how to use web-scraping packages available in python to get football data as efficiently as possible.

This project is written in Python and my webscraper of choice is BeautifulSoup. I've had a little bit of exposure to this already and seems to be the most popular 'web-scraper'. so naturally as safe bet.

For the data source, I've gone with FBREF, very popular with the football hipsters and kids on twitter that comment 'ykb' under posts they agree with. 
The underlying data for FBREF is provided by StatsBomb, so A* for reliabilty and accuracy.
There is vast amount of this data available at league, team, player and match level, complete with deatiled metrics such as pass types and even body parts used for passes. The issue is being able to programtically sift through the webpages to get there. 

The end goal of this is to:

- Create a set of working functions to aggregate data from FBREF.

- Perform a series of data munging tasks to get easy to to use datasets ready for analysis.

- Create a series of Data Visualisations from these cleaned datasets.

- Assess the meaningful metrics we need to start making some predictions on player suitability to positions.


<!-- To prevent this sounding more like an absctract, let get into the fun stuff.  -->


## Setup

First we have to install Beautiful Soup. The beautiful soup package will find the tables we need in the source code of the html. The following [article]( https://smehta.medium.com/scrape-and-create-your-own-beautiful-dataset-from-sports-reference-com-using-beautifulsoup-python-c26d6920684e) goes in to great depths as to how the package works and how you can find the tables you need.

```python
pip install beautifulsoup4

Collecting beautifulsoup4
  Downloading beautifulsoup4-4.10.0-py3-none-any.whl (97 kB)
     |████████████████████████████████| 97 kB 13.1 MB/s            
Collecting soupsieve>1.2
  Downloading soupsieve-2.3.1-py3-none-any.whl (37 kB)
Installing collected packages: soupsieve, beautifulsoup4
Successfully installed beautifulsoup4-4.10.0 soupsieve-2.3.1
WARNING: You are using pip version 21.3.1; however, version 22.0.4 is available.
You should consider upgrading via the '/usr/local/bin/python3 -m pip install --upgrade pip' command.
Note: you may need to restart the kernel to use updated packages.
```


Next up, we import all our necessary packages for web-scraping, data cleaning and analysis.

```python
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import numpy as np
from math import pi
from urllib.request import urlopen
import matplotlib.patheffects as pe
from highlight_text import fig_text
from adjustText import adjust_text
```


## Data 

Let's load the data. For the sake of ease lets start with a squad page. I've gone with this as this page seems to have the most data in a table that is easy for the scrapper to access and retrieve the infomation from. I'm watching far more Serie A these days so the team I've gone with is Napoli. The fbref page used can be found [here](https://fbref.com/en/squads/d48ad4ff/Napoli-Stats).  

![Napoli_Team](/Users/stephenahiabah/Desktop/GitHub/Webs-scarping-for-Fooball-Data-/Napoli Team.png)

 The first function requires the URL of squad to be passed, in order to return a pandas dataframe with the high level per/90 team stats available on this page.

```python
def generate_squadlist(url): 
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
```


The above functions works on any page with this template so effectly any teams stats page will work with this function. 

I want to be able to get the team name and store it for later. As it happens the URLs for FBREF follow a similar pattern so we can slice the list to get the name and save it in the team name variable.


```python
team = "https://fbref.com/en/squads/d48ad4ff/Napoli-Stats"
team_name = team[37:-6]
squad_stats_per_team = generate_squadlist(team)
squad_stats_per_team.head()
```

Now lets have a look a the output 

+---+-----+----+--------+----+----+-------+------+---+---+---+---+---+---+---+------+------+------+------+------+-----+-----+-----+-----+------+------+------+------+------+---------------------+\n| 0 | ITA | DF | 28-224 | 29 | 29 | 2,531 | 28.1 | 1 | 2 | 1 | 0 | 0 | 3 | 0 | 0.04 | 0.07 | 0.11 | 0.04 | 0.11 | 1   | 1   | 2.5 | 3.5 | 0.04 | 0.09 | 0.12 | 0.04 | 0.12 | Giovanni Di Lorenzo |\n+---+-----+----+--------+----+----+-------+------+---+---+---+---+---+---+---+------+------+------+------+------+-----+-----+-----+-----+------+------+------+------+------+---------------------+\n| 1 | POR | DF | 30-293 | 26 | 26 | 2,304 | 25.6 | 0 | 3 | 0 | 0 | 0 | 7 | 0 | 0    | 0.12 | 0.12 | 0    | 0.12 | 1.3 | 1.3 | 2.6 | 4   | 0.05 | 0.1  | 0.15 | 0.05 | 0.15 | Mário Rui           |\n+---+-----+----+--------+----+----+-------+------+---+---+---+---+---+---+---+------+------+------+------+------+-----+-----+-----+-----+------+------+------+------+------+---------------------+\n| 2 | KVX | DF | 28-020 | 26 | 26 | 2,297 | 25.5 | 3 | 0 | 3 | 0 | 0 | 4 | 0 | 0.12 | 0    | 0.12 | 0.12 | 0.12 | 3.2 | 3.2 | 0.2 | 3.5 | 0.13 | 0.01 | 0.14 | 0.13 | 0.14 | Amir Rrahmani       |\n+---+-----+----+--------+----+----+-------+------+---+---+---+---+---+---+---+------+------+------+------+------+-----+-----+-----+-----+------+------+------+------+------+---------------------+\n| 3 | COL | GK | 33-197 | 25 | 25 | 2,250 | 25   | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0    | 0    | 0    | 0    | 0    | 0   | 0   | 0   | 0   | 0    | 0    | 0    | 0    | 0    | David Ospina        |\n+---+-----+----+--------+----+----+-------+------+---+---+---+---+---+---+---+------+------+------+------+------+-----+-----+-----+-----+------+------+------+------+------+---------------------+\n| 4 | POL | MF | 27-300 | 27 | 23 | 1,742 | 19.4 | 5 | 5 | 5 | 0 | 0 | 1 | 0 | 0.26 | 0.26 | 0.52 | 0.26 | 0.52 | 2.8 | 2.8 | 2.9 | 5.7 | 0.14 | 0.15 | 0.3  | 0.14 | 0.3  | Piotr Zieliński     |\n+---+-----+----+--------+----+----+-------+------+---+---+---+---+---+---+---+------+------+------+------+------+-----+-----+-----+-----+------+------+------+------+------+---------------------+


Okay so we've got a table with some good data. There 29 features availble including all of the match related stats in per 90 format. We even have ages and squad time. [Abhishek Sharma](https://sharmaabhishekk.github.io/projects/) provided some inspiration with his [notebook](https://sharmaabhishekk.github.io/mpl-footy/main/2021/08/09/squad-age-profile.html), where he creates a beautiful age-squad profile map. 

Lets do similar but use the dataset we have loaded in and put it in to a function.


```python
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

```


![Napoli_Age_Squad_Chart](Napoli_Age_Squad_Chart.png)


I'm an arsenal fan so ages curves are all the rage right now and I can safely say, this Napoli squad does not look future ready. I've gone with the peak Age range of 24 to 28.5 as this gives us just the right catchment for all players at elite level. 

As we can see there's a troubling distribution here. Napoli have a hight proprtion of players just about to exit their peak or past their peak with a siginifant share of league minutes. From just an eye ball I can see regular starters like Koulibaly, Di Lorenzo very much on the 'wrong side of 30'. Obviously there are limitations, a few are:

- We need to get the age profile of the league for a true comparison
- Not all peaks are equal, goalkeepers, defender have much later peaks than forward players 
- This doesnt account for injury records to clearly explain the factors effecting share of minutes.

A good start but lets go further. 

Lets see if we can take some fixture data from another table in FBREF.

![Napoli_Fixtures](Napoli_Fixture.png)

We're going to write a similar function to what was used for the squad data scrape however we need to contruct a table with a new shape and new features. 

```python

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
```
To clean up the table slightly were going to select only league games and games that have been played. I used the captain column as the logic to filter as if there's no captain the game has not been played yet.

```python

league_results = team_fixture_data("https://fbref.com/en/squads/d48ad4ff/2021-2022/matchlogs/all_comps/schedule/Napoli-Scores-and-Fixtures-All-Competitions")
league_results = league_results.loc[(league_results['captain'] != '') & (league_results['comp'] == 'Serie A')]
league_results 
```

'+---+-----+-------+---------+---+-----------+-------+-----+--------+----------------------+---+------+-----------------+-----+----+---+\n| 0 | 0.5 | 20:45 | Serie A | 2 | Venezia   | 4-3-3 | Sun | 20,000 | Gianluca Aureliano   | W | Home | Lorenzo Insigne | 2.3 | 56 | 0 |\n+---+-----+-------+---------+---+-----------+-------+-----+--------+----------------------+---+------+-----------------+-----+----+---+\n| 1 | 0.6 | 18:30 | Serie A | 2 | Genoa     | 4-3-3 | Sun | 20,000 | Marco Di Bello       | W | Away | Lorenzo Insigne | 1.1 | 61 | 1 |\n+---+-----+-------+---------+---+-----------+-------+-----+--------+----------------------+---+------+-----------------+-----+----+---+\n| 2 | 1   | 18:00 | Serie A | 2 | Juventus  | 4-3-3 | Sat | 23,500 | Massimiliano Irrati  | W | Home | Lorenzo Insigne | 2.1 | 67 | 1 |\n+---+-----+-------+---------+---+-----------+-------+-----+--------+----------------------+---+------+-----------------+-----+----+---+\n| 4 | 0.3 | 20:45 | Serie A | 4 | Udinese   | 4-3-3 | Mon | 11,484 | Gianluca Manganiello | W | Away | Lorenzo Insigne | 2.4 | 63 | 0 |\n+---+-----+-------+---------+---+-----------+-------+-----+--------+----------------------+---+------+-----------------+-----+----+---+\n| 5 | 0.6 | 18:30 | Serie A | 4 | Sampdoria | 4-3-3 | Thu | 4,596  | Paolo Valeri         | W | Away | Lorenzo Insigne | 2.2 | 52 | 0 |\n+---+-----+-------+---------+---+-----------+-------+-----+--------+----------------------+---+------+-----------------+-----+----+---+'



## Conclusion

The success of GPT-3 has spun up a lot of debate as to whether these enormous language models have an 'understanding' of words, know what concepts mean and can reason. Some say it doesn't matter and for a lot of purposes I agree, it doesn't. However when discussing AGI, I think it does and even with GPT-3 you don't have to look too far to 'fool' it. What our little experiment above shows is that a GPT can pick up corelations in the text at many different levels - each layer or set of attention heads may learn relations between words or even 'concepts', style, grammar, maths and more - *if it is there in the text*. But these models can't go further than what might be in the text for now...

Lastly, minGPT is a really outstanding resource for learning about transformers - understanding the theory is one thing but then seeing it coded can often be completely different and you gain a lot from seeing a big model like this broken down so well. Plus, a bonus is that its in PyTorch!








