import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine, correlation


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

def item_similarity(movieName): 
    """
    recomendates similar movies
    INPUT:param data: name of the movie 
   """
    try:
        user_inp=movieName
        inp=df_movies[df_movies['title']==user_inp].index.tolist()
        inp=inp[0]

        df_movies['similarity'] = ratings_matrix_items.iloc[inp]
        df_movies.columns = ['movie_id', 'title', 'release_date','similarity']
    except:
        print("Sorry, the movie is not in the database!")

def recommendedMoviesAsperItemSimilarity(user_id):
    """
    Recommending movie which user hasn't watched as per Item Similarity
    INPUT:param user_id: user_id to whom movie needs to be recommended
    OUTPUT:return: movieIds to user 
    """
    user_movie= df_movies_ratings[(df_movies_ratings.userId==user_id) & df_movies_ratings.rating.isin([5,1])][['title']]
    user_movie=user_movie.iloc[0,0]
    item_similarity(user_movie)
    sorted_movies_as_per_userChoice=df_movies.sort_values( ["similarity"], ascending = False )
    sorted_movies_as_per_userChoice=sorted_movies_as_per_userChoice[sorted_movies_as_per_userChoice['similarity'] >=0.35]['movie_id']
    recommended_movies=list()
    df_recommended_item=pd.DataFrame()
    user2Movies= df_ratings[df_ratings['userId']== user_id]['movieId']
    for movieId in sorted_movies_as_per_userChoice:
            if movieId not in user2Movies:
                df_new= df_ratings[(df_ratings.movieId==movieId)]
                df_recommended_item=pd.concat([df_recommended_item,df_new])
            best10=df_recommended_item.sort_values(["rating"], ascending = False )[1:10] 
    return best10['movieId']

def movieIdToTitle1(listMovieIDs):
    """
    Converting movieId to titles
    INPUT:param user_id: List of movies
    OUTPUT:return: movie titles
    """
    movie_titles= list()
    print(df_movies.head())
    for id in listMovieIDs:
        Counter = df_movies[df_movies['movie_id']==id]['title'].values
        movie_titles.append(Counter[0])
    return movie_titles

