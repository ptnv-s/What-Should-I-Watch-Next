import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine, correlation


df_movies = pd.read_csv("movies.csv")
df_ratings = pd.read_csv("ratings.csv")
df_links = pd.read_csv("links.csv")
df_tags = pd.read_csv("tags.csv")

def cold_start_check(userid):
    df_counter=df_ratings["userId"].unique().tolist()
    print(df_counter)
    if((userid not in df_counter)==1):
        
        x=df_ratings.groupby('movieId').rating.mean()
        
        movie = pd.merge(df_movies,x,how='outer',on='movieId')
        
        movie['rating'].fillna('0',inplace=True)
        x = df_ratings.groupby('movieId',as_index=False).userId.count()
        x.sort_values('userId',ascending=False,inplace=True)
        
        y = pd.merge(movie,x,how='outer',on='movieId')
        y.sort_values(['userId','rating'],ascending=False,inplace=True)
        y = y['title'].values.tolist()
        y = y[0:10]
        return y
    else:
        return 0
