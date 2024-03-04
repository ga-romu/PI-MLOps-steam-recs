# Functions to use in main.py

# import libraries
import pandas as pd
import numpy as np
import json


# Data to use
df_games = pd.read_parquet('data/df_games.parquet')
df_userdata = pd.read_parquet('data/df_userdata.parquet')

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



##################################



def userdata(user_id: str):

    # Filter user_items by user_id
    user_items = df_userdata.loc[df_userdata['user_id'] == user_id]

    # Calculate money spent
    money_spent = user_items['price'].sum()

    # Get the number of items
    number_of_items = float(user_items['items_count'].unique()[0])

    # Filter and count only True values (recommendations)
    user_recommendations = user_items['recommend']
    recommend_rate = user_recommendations.where(user_recommendations == True).count() 

    # Calculate total items to avoid division by zero
    total_items = user_items['items_count'].sum()

    # Calculate recommendation rate (avoiding division by zero)
    recommend_rate = recommend_rate / total_items if total_items > 0 else 0

    user_data = {
        'user id': user_id,
        'money spent': round(money_spent, 2),
        'number of items': number_of_items,
        'recommend rate': round(recommend_rate,3)
    }
    return user_data

