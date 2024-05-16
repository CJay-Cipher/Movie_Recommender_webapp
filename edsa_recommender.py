"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import requests
import base64
import re as reg

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# other app page details
from utils.faq import faq
from utils.about import about_us

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')

dataset = st.container()

# App declaration
def main():
    def clean_movie_titles(titles):
        api_key = "87d991ea"

        # Define a regular expression to match non-alphabetical characters
        regex = reg.compile('[^a-zA-Z ]')

        # Clean each title in the list by removing non-alphabetical characters
        for title in titles:
            cleaned_title = regex.sub('', title)
            if cleaned_title:
                try:
                    url = f"http://www.omdbapi.com/?t={cleaned_title}&apikey={api_key}"
                    re = requests.get(url)
                    re = re.json()
                    
                    col1, col2= st.columns([1, 2])
                    with col1:
                        st.image(re["Poster"])
                    with col2:
                        st.subheader(re["Title"])
                        st.caption(f"GENRE: {re['Genre']}")
                        st.caption(f"YEAR: {re['Year']}")
                        st.caption(f"ACTORS: {re['Actors']}")
                        st.write(re["Plot"])
                        # st.progress(float(re['imdbRating']) / 10)
                        st.text(f"IMDB Rating: {float(re['imdbRating'])}")
                except:
                    # we use pass only when the title is invalid or cannot be found IMDB database
                    pass

    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    
    
    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview", "About Us", "FAQ"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        
        add_bg_from_local('resources/imgs/recommend2.jpg')

        # Header contents
        st.image('resources/imgs/name_image.png',use_column_width=True)
        st.write('## Movie Recommender Engine')
        
        # st.image('resources/imgs/main_image.png',use_column_width=True)
        st.image('resources/imgs/main_image.png',use_column_width=True)
        st.image('resources/imgs/main_image2.png',use_column_width=True)

        

        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[:799])
        movie_2 = st.selectbox('Second Option',title_list[800:1599])
        movie_3 = st.selectbox('Third Option',title_list[1600:2400])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=13)
                    st.title("We think you'll like:")
                    clean_movie_titles(top_recommendations)
                    # for i,j in enumerate(top_recommendations):
                    #     st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                            top_n=13)
                    st.title("We think you'll like:")
                    clean_movie_titles(top_recommendations)
                    # for i,j in enumerate(top_recommendations):
                    #     st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    elif page_selection == "Solution Overview":
        add_bg_from_local('resources/imgs/background3.jpg')
        with dataset:
            st.title("Solution Overview")
            st.subheader("Insights on the Movie dataset")

            st.image("resources/visuals/ratings.png")
            st.image("resources/visuals/genre_count.png")
            st.image("resources/visuals/yearly_movies.png")
            st.image("resources/visuals/yearly_avg.png")
            st.image("resources/visuals/word_cloud2.png")
            st.image("resources/visuals/popular_movies.png")
            st.image("resources/visuals/rated_directors.png")
            st.image("resources/visuals/top_actors.png")


    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.

    elif page_selection == "About Us":
        add_bg_from_local('resources/imgs/rec_app.jpg')
        st.title("About Us")
        st.markdown(about_us)
        st.header("Meet The Team")
        st.image('resources/imgs/team_bm2.png',use_column_width=True)
    
    elif page_selection == "FAQ":
        add_bg_from_local('resources/imgs/recommend2.jpg')
        st.title("Frequently Asked Questions")
        faq_select = st.selectbox("Select from the dropdown below", list(faq.keys()))
        st.markdown(faq[faq_select])
        
    st.sidebar.image("resources/imgs/main9.jpg", use_column_width=True)

        
if __name__ == '__main__':
    main()
