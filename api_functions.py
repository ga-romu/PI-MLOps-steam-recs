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


def developer(desarrollador):

    # Filtra el dataframe por desarrollador de interés
    data_filtrada = df_developer[df_developer['developer'] == desarrollador]
    # Calcula la cantidad de items por año
    cantidad_por_año = data_filtrada.groupby('release_year')['item_id'].count()
    # Calcula la cantidad de elementos gratis por año
    cantidad_gratis_por_año = data_filtrada[data_filtrada['price'] == 0.0].groupby('release_year')['item_id'].count()
    # Calcula el porcentaje de elementos gratis por año
    porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

    result_dict = {
        'cantidad_por_año': cantidad_por_año.to_dict(),
        'porcentaje_gratis_por_año': porcentaje_gratis_por_año.to_dict()
    }
    
    return result_dict

def userdata(user_id):
    '''
    Esta función devuelve información sobre un usuario según su 'user_id'.
         
    Args:
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'cantidad_dinero' (int): Cantidad de dinero gastado por el usuario.
            - 'porcentaje_recomendacion' (float): Porcentaje de recomendaciones realizadas por el usuario.
            - 'total_items' (int): Cantidad de items que tiene el usuario.
    '''
    # Filtra por el usuario de interés
    usuario = df_reviews[df_reviews['user_id'] == user_id]
    # Calcula la cantidad de dinero gastado para el usuario de interés
    cantidad_dinero = df_userdata[df_userdata['user_id']== user_id]['price'].iloc[0]
    # Busca el count_item para el usuario de interés    
    count_items = df_userdata[df_userdata['user_id']== user_id]['items_count'].iloc[0]
    
    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = usuario['reviews_recommend'].sum()
    # Calcula el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews['user_id'].unique())
    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100
    
    return {
        'cantidad_dinero': int(cantidad_dinero),
        'porcentaje_recomendacion': round(float(porcentaje_recomendaciones), 2),
        'total_items': int(count_items)
    }

def userforgenre(genero):
    '''
    Esta función devuelve el top 5 de usuarios con más horas de juego en un género específico, junto con su URL de perfil y ID de usuario.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        dict: Un diccionario que contiene el top 5 de usuarios con más horas de juego en el género dado, junto con su URL de perfil y ID de usuario.
            - 'user_id' (str): ID del usuario.
            - 'user_url' (str): URL del perfil del usuario.
    '''
    # Filtra el dataframe por el género de interés
    data_por_genero = df_genre[df_genre['genres'] == genero]
    # Agrupa el dataframe filtrado por usuario y suma la cantidad de horas
    top_users = data_por_genero.groupby(['user_url', 'user_id'])['playtime_forever'].sum().nlargest(5).reset_index()
    
    # Se hace un diccionario vacío para guardar los datos que se necesitan
    top_users_dict = {}
    for index, row in top_users.iterrows():
        # User info recorre cada fila del top 5 y lo guarda en el diccionario
        user_info = {
            'user_id': row['user_id'],
            'user_url': row['user_url']
        }
        top_users_dict[index + 1] = user_info
    
    return top_users_dict


def best_developer_year(year: int):

    df_year = df_developer[df_developer['release_year'] == year]
    top_devs = (df_year.groupby('developer')['recommend'].count().reset_index().sort_values(by='recommend', ascending=False).head(3))

    rankings = ["1st place", "2nd place", "3rd place"]
    top_devs_dict = dict(zip(rankings, top_devs.to_dict('records')))

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