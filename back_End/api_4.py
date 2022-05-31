import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine, correlation


#BASIC OPERATIONS
df_movies = pd.read_csv("movies.csv")
df_ratings = pd.read_csv("ratings.csv")
df_links = pd.read_csv("links.csv")
df_tags = pd.read_csv("tags.csv")
df_movies['genres'] = df_movies['genres'].replace(to_replace="(no genres listed)", value="")
df_movies_ratings=pd.merge(df_movies, df_ratings)
ratings_matrix_items = df_movies_ratings.pivot_table(index=['movieId'],columns=['userId'],values='rating').reset_index(drop=True)
ratings_matrix_items.fillna( 0, inplace = True )
movie_similarity = 1 - pairwise_distances( ratings_matrix_items.values, metric="cosine" )
np.fill_diagonal( movie_similarity, 0 )
ratings_matrix_items = pd.DataFrame( movie_similarity )
ratings_matrix_users = df_movies_ratings.pivot_table(index=['userId'],columns=['movieId'],values='rating').reset_index(drop=True)
ratings_matrix_users.fillna( 0, inplace = True )
movie_similarity = 1 - pairwise_distances( ratings_matrix_users.values, metric="cosine" )
np.fill_diagonal( movie_similarity, 0 )
ratings_matrix_users = pd.DataFrame( movie_similarity )
similar_user_series= ratings_matrix_users.idxmax(axis=1)
df_similar_user= similar_user_series.to_frame()

#RECOMMENDATION FUNCTIONS

def movieIdToTitle2(listMovieIDs):
    """
    Converting movieId to titles
    INPUT:param user_id: List of movies
    OUTPUT:return: movie titles
    """
    movie_titles= list()
    print(df_movies.head())
    for id in listMovieIDs:
        #movie_titles.append(df_movies[df_movies['movieId']==id]['title']) #eerror
        Counter = df_movies[df_movies['movieId']==id]['title'].values
        movie_titles.append(Counter[0])
    return movie_titles

movieId_recommended=list()
def getRecommendedMoviesAsperUserSimilarity(userId):

    """
    Recommending movies which user hasn't watched as per User Similarity
    INPUT:param user_id: user_id to whom movie needs to be recommended
    OUTPUT:return: movieIds to user 
    """

    user2Movies= df_ratings[df_ratings['userId']== userId]['movieId']
    sim_user=df_similar_user.iloc[0,0]
    df_recommended=pd.DataFrame(columns=['movieId','title','genres','userId','rating','timestamp'])
    for movieId in df_ratings[df_ratings['userId']== sim_user]['movieId']:
        if movieId not in user2Movies:
            df_new= df_movies_ratings[(df_movies_ratings.userId==sim_user) & (df_movies_ratings.movieId==movieId)]
            df_recommended=pd.concat([df_recommended,df_new])
        best10=df_recommended.sort_values(['rating'], ascending = False )[1:10]  
    return best10['movieId']

