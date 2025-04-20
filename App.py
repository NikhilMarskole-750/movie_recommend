import streamlit as st
import pickle
import requests

# Load data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

OMDB_API_KEY = "2c51ef8a"

# Function to fetch poster
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Poster") and data["Poster"] != "N/A":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Image"

# Recommend function
def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []
    trailer_links = []

    for i in movie_list:
        title = movies.iloc[i[0]]['title']
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))
        trailer_links.append(f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+trailer")

    return recommended_titles, recommended_posters, trailer_links

# Page setup
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .centered {
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-poster:hover {
        filter: brightness(1.1);
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3);
        transition: 0.3s ease;
    }
    .movie-caption {
        text-align: center;
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<h1 class="centered">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)

# Dropdown
selected_movie = st.selectbox("🎞️ Select a movie you like:", movies['title'].values)

# Button
if st.button("Recommend"):
    with st.spinner("Fetching awesome recommendations..."):
        titles, posters, links = recommend(selected_movie)

        st.markdown('<h2 class="centered">Top 5 Recommendations</h2>', unsafe_allow_html=True)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <a href="{links[idx]}" target="_blank">
                        <img src="{posters[idx]}" class="movie-poster" width="100%" style="border-radius: 12px;" />
                    </a>
                    <div class="movie-caption">{titles[idx]}</div>
                    """,
                    unsafe_allow_html=True
                )
