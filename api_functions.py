# Functions to use in main.py

# import libraries
import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity


# Data to use
df_games = pd.read_parquet('data/df_games.parquet')
df_userdata = pd.read_parquet('data/df_userdata.parquet')
df_developer = pd.read_parquet('data/df_developer.parquet')
df_genre = pd.read_parquet('data/df_genre.parquet')
df_rec = pd.read_parquet('data/df_rec.parquet')



def homepage():
    '''
    Generates an HTML homepage for the Steam API for video game queries.
    
    Returns:
    str: HTML code displaying the homepage.
    '''
    return '''
    <html>
        <head>
            <title>Steam API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Steam Video Game Queries API</h1>
            <p>Welcome to the Steam API where various queries about the gaming platform can be made.</p>
            <p>INSTRUCTIONS:</p>
            <p>Type <span style="background-color: lightgray;">/docs</span> after the current URL of this page to interact with the API.</p>
            <p>Visit my profile on <a href="https://www.linkedin.com/in/g-a-ro-mu/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin"></a></p>
            <p>The development of this project is on <a href="https://github.com/ga-romu/PI-MLOps-steam-recs"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
        </body>
    </html>
    '''


##################################

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

##################################


def UserForGenre(genre:str):

  # Filter data for the given genre
  genre_data = df_genre[df_genre['genres'] == genre]

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
      "genre": genre,
      "user_id": top_user_id,
      "Hours played": playtime_details
  }



##################################

def best_developer_year(year:int):
  
    df_year = df_developer[df_developer['release_year'] == year]
    top_devs = (df_year.groupby('developer')['recommend'].count().reset_index().sort_values(by='recommend', ascending=False).head(3))

    rankings = ["1st place", "2nd place", "3rd place"]
    top_devs_dict = dict(zip(rankings, top_devs.to_dict('records')))

    return top_devs_dict

##################################


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


##################################

def recomendacion_juego(id: int):
    
    # Verificamos si el juego con game_id existe en df_games
    game = df_rec[df_rec['id'] == id]

    if game.empty:
        return("El juego '{id}' no posee registros.")
    
    # Obtenemos el índice del juego dado
    idx = game.index[0]

    # Tomamos una muestra aleatoria del DataFrame df_games
    sample_size = 2000  # Definimos el tamaño de la muestra (ajusta según sea necesario)
    df_sample = df_rec.sample(n=sample_size, random_state=42)  # Ajustamos la semilla aleatoria según sea necesario

    # Calculamos la similitud de contenido solo para el juego dado y la muestra
    sim_scores = cosine_similarity([df_rec.iloc[idx, 3:]], df_sample.iloc[:, 3:])

    # Obtenemos las puntuaciones de similitud del juego dado con otros juegos
    sim_scores = sim_scores[0]

    # Ordenamos los juegos por similitud en orden descendente
    similar_games = [(i, sim_scores[i]) for i in range(len(sim_scores)) if i != idx]
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)

    # Obtenemos los 5 juegos más similares
    similar_game_indices = [i[0] for i in similar_games[:5]]

    # Listamos los juegos similares (solo nombres)
    similar_game_names = df_sample['title'].iloc[similar_game_indices].tolist()

    return {"similar_games": similar_game_names}