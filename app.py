import string
import streamlit as st
import json
from operator import itemgetter
import requests
from PIL import Image
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
import pandas as pd
endpoint0 = 'http://127.0.0.1:8000/api0'
endpoint1 = 'http://127.0.0.1:8000/api1' 
endpoint2 = 'http://127.0.0.1:8000/api2'
endpoint3 = 'http://127.0.0.1:8000/api3'
endpoint4 = 'http://127.0.0.1:8000/api4'
endpoint5 = 'http://127.0.0.1:8000/api5'

img = Image.open('./images/favicon.png')
st.set_page_config(page_title='Movie Recommender Engine' , page_icon=img , layout="centered",initial_sidebar_state="expanded")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: visible;}
            footer:after{
                background-color:#99CCCC;
                font-size:12px;
                font-weight:8px;
                height:30px;
                margin:1rem;
                padding:0.8rem;
                content:'By Pratinav Seth - 200968216';
                display: flex;
                align-items:center;
                justify-content:center;
                color:black;
            }
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
lottie_contact =load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_dhcsd5b5.json")
lottie_loadLine =load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_yyjaansa.json")
lottie_github =load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_S6vWEd.json")



with st.sidebar:
    selected = option_menu(
                menu_title="Movie Recommendation",  
                options=["Home", "About", "Github-Repo"],  
                icons=["house", "person-square", "github"],  
                menu_icon="cast",  
                default_index=0,  
                 styles={
                "container": {"padding": "3", "background-color": "#f0f2f6" , "Font-family":"Monospace"},
                "icon": {"color": "#31333f", "font-size": "25px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px","Font-family":"Monospace"},
                "nav-link-selected": {"background-color": "#AFB5DA"},
                }
                )

    if selected == "Home":
      st.empty()
    
    if selected == "About":
        st.markdown("""<div style='
            background-color:#99CCCC; 
            padding:1rem;
            font-size:17px;
            border-radius:8px;
            text-align: justify;
           '>
Build an app with a simple UI which will allow the user to search for movies and give recommendations based on the user and the movie searched for by use of content based and collaborative filtering.
</div>
        <br>
       """
        ,unsafe_allow_html=True,)

# The github repo code.
            
    if selected == "Github-Repo":  
        st_lottie(lottie_github,height=150,width=270,key="coding5")
        st.subheader("Check Out The Github Repository For Movie Recommender Engine")
        st.markdown(
            """
            <div style='
            background-color:#99CCCC; 
            cursor:pointer; 
            height:2.8rem;
            font-size:25px;
            font-weight:bolder;
            border-radius:5px;
            font-family: Helvetica, sans-serif;
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
            display: flex;
            align-items:center;
            justify-content:center;'>
                    <a  href="https://github.com/ptnv-s/Movie_Recommendation_System" 
                    style='color: black; 
                           text-decoration:none;
                           padding-top:6px;
                           padding-bottom:5px;
                           text-align:center;'>
                    GITHUB
                    </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    
    df_movies = pd.read_csv("back_End/movies.csv")
    #df_movies['title'] = df_movies['title'].astype(string)
    movies = df_movies['title'].unique().tolist()
    #Designing of the header and main section of the application.
    with st.container():
     left_column, right_column = st.columns(2)
     with left_column:
            st.write("")
            st.title('MOVIE RECOMMENDER ENGINE') 
     with right_column:
            st_lottie(lottie_coding, height=300,width=400, key="coding")
        
    
    
    apps = ['*--Select--*','Movie based','UserId']   
    app_options = st.selectbox('Method Of Recommendation:', apps)


    
    if app_options == 'Movie based':
        movie_select = st.selectbox('Select a movie:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('Select a movie')
        else:
            c_movie = str(movie_select)
            st.markdown("Recommending movies based on search made by user by comparing similarities between genres")
            st.markdown("Since you like the below Movie")
            print(type(c_movie))
            search_c = "https://www.google.com/search?q="
            c_var = str(search_c + movie_select)
            c_var = c_var.replace(" ", "_")
            st.markdown(f"- {movie_select} Link - [link]({c_var})")
            print(movie_select)
            output1 = requests.get(endpoint1, json={"movie_title": str(c_movie)},verify=False)
            output_c1 = output1.json()
            print("hii")
            print(output_c1)
            st.markdown("You will like the following Movies")
            i=0
            for counter in output_c1['recommendation']:
                c_var = str(search_c + counter)
                c_var = c_var.replace(" ", "_")
                st.markdown(f"- {counter} Link - [link]({c_var})")
                i=i+1
                if(i==10):
                    break

        
                        
    if app_options == apps[2]:
        options = st.number_input('Enter UserId',min_value=0, max_value=100000, value=0, step=1)
        output = requests.get(endpoint0, json={"userid": options},verify=False)
        output_c = output.json()
        if(output_c["recommendation"]==0):
            st.markdown("Recommending movies based on previous watch history of a user based on genres of previous movies")
            output2 = requests.get(endpoint2, json={"userid": options},verify=False)
            output_c2 = output2.json()
            search_c = "https://www.google.com/search?q="
            i=0
            for counter in output_c2["recommendation"]:
                c_var = str(search_c + counter)
                c_var = c_var.replace(" ", "_")
                #link='check out this [link](c_var)'
                #st.markdown(link,unsafe_allow_html=True)
                st.markdown(f"- {counter} Link - [link]({c_var})")
                i=i+1
                if(i==10):
                    break
            
            st.markdown("Item-Item Filtering – Given user-id Recommends Movies which isn’t seen by user based on ratings of user towards a movie he had seen")
            output3 = requests.get(endpoint3, json={"userid": options},verify=False)
            output_c3 = output3.json()
            i=0
            for counter in output_c3["recommendation"]:
                print(counter[2])
                c_var = str(search_c + counter)
                c_var = c_var.replace(" ", "_")
                #link='check out this [link](c_var)'
                #st.markdown(link,unsafe_allow_html=True)
                st.markdown(f"- {counter} Link - [link]({c_var})")
                i=i+1
                if(i==10):
                    break

            st.markdown("Item-Item Filtering – Given user-id Recommends Movies which isn’t seen by user based on ratings of user towards a movie he had seen")
            output4 = requests.get(endpoint4, json={"userid": options},verify=False)
            output_c4 = output4.json()
            i=0
            for counter in output_c4["recommendation"]:
                c_var = str(search_c + counter)
                c_var = c_var.replace(" ", "_")
                #link='check out this [link](c_var)'
                #st.markdown(link,unsafe_allow_html=True)
                st.markdown(f"- {counter} Link - [link]({c_var})")
                i=i+1
                if(i==10):
                    break
        
            st.markdown("User-Item Filtering – Given user-id in database tries to find user most similar and then recommends what that user has seen but our user hasn’t")
            output5 = requests.get(endpoint5, json={"userid": options},verify=False)
            output_c5 = output5.json()
            i=0
            for counter in output_c5["recommendation"]:
                c_var = str(search_c + counter)
                c_var = c_var.replace(" ", "_")
                #link='check out this [link](c_var)'
                #st.markdown(link,unsafe_allow_html=True)
                st.markdown(f"- {counter} Link - [link]({c_var})")
                i=i+1
                if(i==10):
                    break
        
        else:
            st.markdown("Recommending top 10 most popular movies if its a new user")
            search_c = "https://www.google.com/search?q="
            for counter in output_c["recommendation"]:
                c_var = str(search_c + counter)
                c_var = c_var.replace(" ", "_")
                #link='check out this [link](c_var)'
                #st.markdown(link,unsafe_allow_html=True)
                st.markdown(f"- {counter} Link - [link]({c_var})")
        


