import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


df_movies = pd.read_csv("movies.csv")
df_ratings = pd.read_csv("ratings.csv")
df_links = pd.read_csv("links.csv")
df_tags = pd.read_csv("tags.csv")
df_ratings.drop(columns='timestamp',inplace=True)
df_tags.drop(columns='timestamp',inplace=True)
tfidf_movies_genres = TfidfVectorizer(token_pattern = '[a-zA-Z0-9\-]+')
df_movies['genres'] = df_movies['genres'].replace(to_replace="(no genres listed)", value="")
tfidf_movies_genres_matrix = tfidf_movies_genres.fit_transform(df_movies['genres'])
cosine_sim_movies = linear_kernel(tfidf_movies_genres_matrix, tfidf_movies_genres_matrix)


def get_recommendations_based_on_genres(movie_title, cosine_sim_movies=cosine_sim_movies):
    idx_movie = df_movies.loc[df_movies['title'].isin([movie_title])]
    idx_movie = idx_movie.index
    sim_scores_movies = list(enumerate(cosine_sim_movies[idx_movie][0]))
    sim_scores_movies = sorted(sim_scores_movies, key=lambda x: x[1], reverse=True)
    sim_scores_movies = sim_scores_movies[1:4]
    movie_indices = [i[0] for i in sim_scores_movies]
    movie_titles= []
    for id in movie_indices:
        try:
            Counter = df_movies[df_movies['movieId']==id]['title'].values
            movie_titles.append(Counter[0])
        except:
            continue
    
    print(movie_titles)
    return set(movie_titles)

def get_recommendation_content_model(userId):
    recommended_movie_list = []
    movie_list = []
    df_rating_filtered = df_ratings[df_ratings["userId"]== userId]
    for key, row in df_rating_filtered.iterrows():
        movie_list.append((df_movies["title"][row["movieId"]==df_movies["movieId"]]).values) 
    for index, movie in enumerate(movie_list):
        for key, movie_recommended in get_recommendations_based_on_genres(movie[0]).iteritems():
            recommended_movie_list.append(movie_recommended)
    for movie_title in recommended_movie_list:
        if movie_title in movie_list:
            recommended_movie_list.remove(movie_title)
    print(recommended_movie_list)
    return set(recommended_movie_list)