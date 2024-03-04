# Functions to use in main.py

# import libraries
import pandas as pd
import numpy as np
import json


# Data to use
df_games = pd.read_parquet('data/df_games.parquet')


class DataFrameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.DataFrame):
            # Convert DataFrame to a list of dictionaries
            return obj.to_dict(orient='records')
        return json.JSONEncoder.default(self, obj)
    
def developer(developer:str):
    # Filter the dataframe by developer
    df_dev = df_games[df_games['developer'] == developer]
    
    # Calculate the quantity of items released by year
    items_by_year = df_dev.groupby(df_dev['release_year'])['id'].count()
    
    # Calculate the percentage of free content
    free_content_by_year = (df_dev[df_dev['price'] == 0].groupby(df_dev['release_year'])['id'].count() / items_by_year * 100).fillna(0)
    
    # Create a dataframe with the results
    df_result = pd.DataFrame({'Year': items_by_year.index, 'Items Released': items_by_year.values, '% of Free Content': free_content_by_year.values})
    
    return json.dumps(df_result, cls=DataFrameEncoder)
