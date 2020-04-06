# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 00:33:55 2020

@author: jeanb
"""

import os
import pandas as pd
import numpy as np
import re

path_data = r"C:\Users\jeanb\Desktop\Cours\Cours Ironhack\Projets\Projet_week_2\steam-games-complete-dataset"

steam = pd.read_csv(path_data+"/steam_games.csv")

os.chdir(r"C:\Users\jeanb\Desktop\Cours\Cours Ironhack\Projets\Projet_week_2")

### FUNCTIONS TO MODIFY COLUMNS : GENRE, RELEASE_DATE, ORIGINAL_PRICE

# Filter GENRE

def filter_first_genre(s): 

    res = ""
    
    not_genre = ["Free to Play","Nudity","Sexual Content","Violent","Early Access","Gore"]
    
    genre_to_other = ["Valve","Animation & Modeling","Utilities","Design & Illustration",
                  "Video Production","Audio Production","Web Publishing","Movie","Accounting",
                  "Software Training","Photo Editing","Game Development","Short","HTC"]

    lst = str(s).split(",")

    to_remove = [e for e in lst if e in not_genre]

    for e in to_remove:
        lst.remove(e)
    
    if len(lst) > 0:
        res = lst[0]
        
        if res in genre_to_other:
            res = "Other"
            
    if res in ["", "nan"]:
        res = "unknown"
            
    return res

def filter_genre(steam):

    steam.genre = steam.genre.apply(lambda x : filter_first_genre(x))

    return steam

# Filter RELEASE_DATE
    
def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def get_year(s):
    
    s=str(s)
    
    y = re.findall('(\d{4})', s)
    
    if len(y) != 0:
    
        res = y[0]
    
        if time_in_range(1980,2020,int(res)) != True:
            
            res = "error_year"
    
    else:
        res = "error_year"
    
    return res

def filter_release_date(steam):
    
    #steam=steam.rename(columns={'release_date':'release_year'})
    
    steam.release_date = steam.release_date.apply(lambda x : get_year(x))

    return steam

# Filter ORIGINAL_PRICE

def filter_original_price(steam):
    
    #steam=steam.rename(columns={'original_price':'free_paying'})
    
    # replace NaN with corresponding value in discount_price column
    steam.original_price = np.where(steam.original_price.isnull(), steam.discount_price, steam.original_price)
    
    # replace remaining NaN with "missing_info"
    steam.original_price = np.where(steam.original_price.isnull(), "missing_info", steam.original_price)
    
    # replace every price with "paying"
    steam.original_price = steam.original_price.apply(lambda x : "paying" if "$" in str(x) else x)
    
    # replace different kinds of free indication by "free"
    steam.original_price = steam.original_price.apply(lambda x : "free" if str(x) in ["Free","Free to Play",
                                                                                 "Free To Play"] else x)
        
    # replace every other kind of values (neither "paying" or "free") with missing_info
    steam.original_price = steam.original_price.apply(lambda x : "missing_info" if str(x) 
                                                  not in ["paying","missing_info","free"] else x)

    return steam

# Filter columns general function
    
def filter_columns(steam):
    
    steam_genre_cleaned = filter_genre(steam)
    
    steam_genre_date_cleaned = filter_release_date(steam_genre_cleaned)
    
    steam_col_cleaned = filter_original_price(steam_genre_date_cleaned)
    
    return steam_col_cleaned

# Select columns

def select_columns(steam):
    
    steam = steam[["types","name","release_date","genre","original_price"]]
    
    return steam

# Filter rows
    
def remove_rows(steam):
    
    # filter types rows
    steam = steam[steam['types'].notna()]
    steam = steam[~steam.types.str.contains("bundle")]
    steam = steam[~steam.types.str.contains("sub")]
    
    # filter name
    steam = steam[steam['name'].notna()]
    
    # filter release_date
    steam = steam[~steam.release_date.str.contains("error_year")]
    
    # filter genre
    steam = steam[~steam.genre.str.contains("unknown")]
    
    # filter original_price
    steam = steam[~steam.original_price.str.contains("missing_info")]
    
    return steam
    
### Full wrangle
    
def wrangle_dataframe(steam):
    
    steam_filtered_col = filter_columns(steam)
    
    steam_selected_filtered_col = select_columns(steam_filtered_col)
    
    steam_fully_wrangled = remove_rows(steam_selected_filtered_col)
    
    return steam_fully_wrangled


### Analyze dataframe and create graph

##### Analysis 1

def analyze1_dataframe(steam):

    grouped = steam.groupby("release_date")["name"].agg("count").reset_index()
    
    analysis = grouped.sort_values("release_date", ascending=False).head(10)
    
    return analysis

def viz1(df):
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set() # simply make the plot looks better
    fig,ax=plt.subplots(figsize=(10,5)) # here we initialize a plot ; everything related to vizualisation that goes after will be on the plot
    barchart=sns.barplot(data=df, x="release_date", y="name")
    plt.title(f"Number of games by years on Steam since 2011")
    return barchart

def save_viz1(plot):

    fig=plot.get_figure()
    fig.savefig(f"number_of_games_by_years_on_steam_since_2011.png")

##### Analysis 2

def analyze2_dataframe(steam):

    steam['COUNTER'] = 1
    
    analysis = steam.groupby(["genre","original_price"])['COUNTER'].sum()
    
    return analysis

def viz2(df):
    
    barchart = df.unstack().plot.bar(figsize=(10,5))
    
    return barchart

def save_viz2(plot):

    fig=plot.get_figure()
    fig.savefig(f"paying_free_games_by_genre.png")


if __name__=="__main__":
    data_prepared = wrangle_dataframe(steam)
    # Analysis 1
    res1 = analyze1_dataframe(data_prepared)
    barchart1 = viz1(res1)
    save_viz1(barchart1)
    # Analysis 2
    res2 = analyze2_dataframe(data_prepared)
    barchart2 = viz2(res2)
    save_viz2(barchart2)
