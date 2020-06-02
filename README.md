# project_2_data_pipeline_steam_dataset
Repository for the 2nd project of Ironhack on data pipeline. This project is on a steam database


### Project Description

The goal was to clean a steam database found on kaggle, to make it more usable, and to make simple statistics about it.

First I decided to focus on simple and general trends to represents with the dataset. The number of games per release date seemed obvious, and
for the distribution of games between free and paying, by genre, it seemed interesting and challenging since it grouped the dataframe by 2 columns.

### Libraries

- os
- pandas
- numpy
- regex

### Cleaning

I started cleaning the column genre. It was a quite difficult to find a way to only get one genre per game, and probably not the best option but I
went for it anyway. I tried to get all the unique genre for the whole column but owing to their number I stood with "only" 12 (+ unknown) unique values.
I also tried to fill the NaN with values from popular_tags for the corresping rows, but I didn't manage to do it properly so I abandonned this idea.

Genre unique values : ['Action', 'Adventure', 'Strategy', 'Indie', 'Simulation', 'Racing', 'RPG', 'Massively Multiplayer', 'Casual', 'unknown',
			'Other', 'Sports', 'Education','unknown']

For the release_date column I used a regex function to get 4 digits elements (that could correspond to a year), and then I filtered on wether the number
was between 1980 and 2020, and if it returned an empty value. In the end I got unique values from 1984 to 2020, and created a value "error_year" for NaN and
non-adequate values.

For the original_price column, my objective was to get a 2 values column with "free" and "paying". I also filled some of the NaN with their corresponding value
in the discount_price column, when it had a price. Eventually I replaced every price with "paying", as much free mentions as possible as "free" and the rest as
"missing_info".

### Selecting columns and removing rows

I then selected the 5 columns that I needed ["types", "name", "release_date", "genre", "original_price"], and removed rows :
- removed the NaN and "bundle"/"sub" rows for the column types
- removed the NaN for the column name
- removed the "error_year" for the column release_date
- removed the "unknown" for the column genre
- removed the "missing_info" for the column original_price

After this step, the dataframe went from 40833 rows and 20 columns to 34150 rows and 5 columns.

### Performing the analysis

First I did the analysis for the number of games per years ; I simply grouped by release_date and aggregated by count, ordered by release_date and select the 10 first.
For the second analysis on the distribution of games between free and paying by genre, I grouped by genre and by original_price, used an additional column filled with 
"1" to get the table properly made for the graph, and grouped by sum.

Once the 2 plots made as wanted, they were saved as .png
