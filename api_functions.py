# Functions to use in main.py

# import libraries
import pandas as pd
import numpy as np
import json


# Data to use
df_games = pd.read_parquet('data/df_games.parquet')
piv_norm = pd.read_parquet('data/piv_norm.parquet')
user_sim_df = pd.read_parquet('data/user_sim_df.parquet')
item_sim_df = pd.read_parquet('data/item_sim_df.parquet')
df_userdata = pd.read_parquet('data/df_userdata.parquet')
df_developer = pd.read_parquet('data/df_developer.parquet')

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

def best_developer_year(year:int):
  
    df_year = df_developer[df_developer['release_year'] == year]
    top_devs = (df_year.groupby('developer')['recommend'].count().reset_index().sort_values(by='recommend', ascending=False).head(3))

    rankings = ["1st place", "2nd place", "3rd place"]
    top_devs_dict = dict(zip(rankings, top_devs.to_dict('records')))

    return top_devs_dict


def developer_reviews_analysis(developer: str):
  """
  Analyzes developer reviews and returns a dictionary with review counts.

  Args:
      developer: The name of the developer to analyze.

  Returns:
      A dictionary with the developer name as the key and a list containing 
      the count of negative and positive reviews as values.
  """

  # Merge reviews and games on item_id and developer
  # Specify how to handle differing column names if needed


  # Count reviews by sentiment category
  review_counts = df_developer['sentiment_category'].value_counts().to_dict()

  # Convert category counts to a list with desired format
  review_list = {
      'Negative' : review_counts.get(0, 0),  # Use integer 0 for negative category
      'Positive' : review_counts.get(2, 0),  # Use integer 2 for positive category
  }

  # Create the dictionary with developer name and review counts
  return {developer: review_list}


def recommendation_user(user_id: str):
  """
  Recommends items (games) to a user based on user-based collaborative filtering.

  Args:
      user_id (str): The ID of the user for whom recommendations are generated.

  Returns:
      list: A list of top 5 recommended item names (games) for the user.
      If the user ID is not found in the data, an empty list is returned.
  """
  # Check if user exists in the data
  if user_id not in piv_norm.columns:
    return [] 

  # Get similar users based on user_similarity dataframe
  similar_users = user_sim_df.sort_values(by=user_id, ascending=False).index[1:11]

  # Get items rated by similar users
  recommended_items = piv_norm.loc[:, similar_users].copy()

  # Remove items already rated by the target user
  if user_id in recommended_items.columns:
    recommended_items.drop(user_id, axis=1, inplace=True)

  # Fill missing values with 0
  recommended_items.fillna(0, inplace=True)

  # Calculate average rating for each item across similar users
  average_ratings = recommended_items.mean(axis=1)

  # Sort items by their average rating and get the top 5
  top_recommendations = average_ratings.sort_values(ascending=False).head(5).index.tolist()

  print(f'Top 5 recommended games for {user_id}: {top_recommendations}')

  return top_recommendations