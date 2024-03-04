# Functions to use in main.py

# import libraries
import pandas as pd
import numpy as np
import json
import operator


# Data to use
df_games = pd.read_parquet('data/df_games.parquet')
df_reviews = pd.read_parquet('data/df_reviews.parquet')
piv_norm = pd.read_parquet('data/piv_norm.parquet')
user_sim_df = pd.read_parquet('data/user_sim_df.parquet')
item_sim_df = pd.read_parquet('data/item_sim_df.parquet')
df_userdata = pd.read_parquet('data/df_userdata.parquet')
df_genre = pd.read_parquet('data/df_genre.parquet')
df_developer = pd.read_parquet('data/df_developer.parquet')

class DataFrameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.DataFrame):
            # Convert DataFrame to a list of dictionaries
            return obj.to_dict(orient='records')
        return json.JSONEncoder.default(self, obj)

def calculate_free_content_percentage(df, column_name):
    """Calculates the percentage of free content in the given DataFrame."""
    free_content = df[df[column_name] == 0].groupby(df[column_name]).count()
    total_content = df.groupby(df[column_name]).count()
    percentage_free_content = (free_content / total_content * 100).fillna(0)
    return percentage_free_content

def developer(developer):
    # Filter the dataframe by developer
    developer_games = df_games[df_games['developer'] == developer]
    
    # Calculate the quantity of items released by year
    items_by_year = developer_games.groupby(developer_games['release_year'])['id'].count()
    
    # Calculate the percentage of free content
    free_content_by_year = calculate_free_content_percentage(developer_games, 'price')
    
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

def UserForGenre(genero:str):

  # Filter data for the given genre
  genre_data = df_genre[df_genre['genres'] == genero]

  # Calculate total playtime per user per year (assuming playtime_forever in minutes)
  user_year_playtime = (
      genre_data
      .groupby(['user_id', genre_data['release_year']])['playtime_forever']
      .sum()
      .apply(lambda x: x / 60)  # Convert minutes to hours
      .reset_index()
  )

  # Group by user ID and sum playtime across years
  user_playtime_total = user_year_playtime.groupby('user_id')['playtime_forever'].sum()

  # Find user with the most playtime
  top_user_id = user_playtime_total.idxmax()

  # Filter data for the top user
  top_user_data = user_year_playtime[user_year_playtime['user_id'] == top_user_id]

  # Prepare playtime details
  playtime_details = [
      {'year': row["release_year"], 'hours': round(row["playtime_forever"], 2)}
      for _, row in top_user_data.iterrows()
  ]

  # Return user details dictionary
  return {
      "genre": genero,
      "user_id": top_user_id,
      "Hours played": playtime_details
  }


def best_developer_year(year: int):

    # Filter the data for the given year
    df_year = df_developer[df_developer['release_year'] == year]

    # Calculate the number of recommendations for each developer
    dev_recommend_counts = df_year['developer'].value_counts()

    # Get the top 3 developers based on the number of recommendations
    top_devs_index = dev_recommend_counts.nlargest(3).index

    # Create a dictionary with the rankings and the corresponding developers
    rankings = ["1st place", "2nd place", "3rd place"]
    top_devs_dict = {rank: {'developer': dev, 'recommend': dev_recommend_counts[dev]} for rank, dev in zip(rankings, top_devs_index)}

    return top_devs_dict


def developer_reviews_analysis(developer):
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