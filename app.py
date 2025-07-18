import streamlit as st
import pandas as pd
import pickle
import lzma
from streamlit_option_menu import option_menu

# --- Page Setup ---
st.set_page_config(page_title="FLIXREC", page_icon="🎬", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    with open('movie_dict_final_1.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    with lzma.open('similarity_compressed.pkl.xz', 'rb') as f:
        similarity = pickle.load(f)
    return pd.DataFrame(movies_dict), similarity

new_df, similarity = load_data()

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    /* Main Content */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #141414;
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50, #1a1a2e) !important;
    }
    .sidebar .sidebar-content {
        color: white !important;
    }
    .sidebar .stMarkdown h2, .sidebar .stMarkdown h3 {
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #e50914;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: background 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #b20710;
    }
    
    /* Cards */
    .recommend-card {
        background-color: #1c1c1c;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    .recommend-card:hover {
        transform: translateY(-5px);
    }
    .recommend-title {
        font-size: 1.5rem;
        color: #e50914;
        margin-bottom: 0.5rem;
    }
    .overview {
        font-size: 1rem;
        color: #cccccc;
        margin-bottom: 0.3rem;
    }
    .crew {
        font-size: 0.9rem;
        color: #aaaaaa;
        font-style: italic;
    }
    .cast {
        font-size: 0.85rem;
        color: #999999;
        margin-top: 0.5rem;
    }
    
    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1c1c1c !important;
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] input {
        color: white !important;
    }
    
    /* Navigation */
    .st-eb {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    # Logo and Title
    try:
        st.image("images/Netflix-Thanks.jpg.png", width=80)
    except:
        st.image("https://img.icons8.com/external-justicon-flat-justicon/64/ffffff/external-movie-film-reel-justicon-flat-justicon.png", 
                width=80)
        
    # Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["Home", "Recommendations", "About"],
        icons=["house", "film", "info-circle"],
        default_index=1,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "16px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "color": "white"},
            "nav-link-selected": {"background-color": "#e50914"},
        }
    )
    
    # About Section
    st.markdown("---")
    st.markdown("### ℹ️ About This App")
    st.markdown("""
    <div style='color: #f0f0f0; font-size: 0.95rem;'>
    This advanced recommender system suggests movies tailored to your preferences using:
    
    <b>Content-Based Filtering</b>:
    <ul>
        <li>Analyzes movie features</li>
        <li>Finds similar content</li>
        <li>Generates personalized recommendations</li>
    </ul>
    
    <b>Dataset</b>: TMDB 5000 Movies<br>
    <b>Algorithm</b>: Cosine Similarity
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='font-size: 0.85rem; color: rgba(255, 255, 255, 0.7); margin-top: 2rem;'>
        <p>Made with ❤️ by <b>Darshan Walher</b></p>
        <p>Contact: <a href="mailto:darshanwalher21@gmail.com" style='color: #e50914;'>darshanwalher21@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Content ---
if selected == "Home":
    st.markdown("""
<h2 style='color: #ffffff;'>🎬 Discover Your Next Favorite Movie</h2>
<p>FLIXREC helps you explore and enjoy personalized movie recommendations using intelligent content analysis.</p>

<h4 style='margin-top: 2rem; color: #e50914;'>🚀 How It Works</h4>
<ol style='line-height: 1.7;'>
    <li>Choose a movie you love from the dropdown list</li>
    <li>Click the <b>"Recommend"</b> button</li>
    <li>Get 5 similar movies based on story, crew, and keywords</li>
</ol>

<p style='margin-top: 2rem;'>Head over to the <b>📽️ Recommendations</b> section from the sidebar to begin!</p>
""", unsafe_allow_html=True)

elif selected == "Recommendations":
    st.markdown("<h1 style='color:#e50914;'>🎬 FLIXREC</h1>", unsafe_allow_html=True)
    st.subheader("Get Top 5 Movie Recommendations Based on Your Favorite Movie")

    # Movie Select
    selected_movie = st.selectbox("🎥 Select a Movie:", new_df['title'].values)

    # Enhanced Recommendation Function with Cast
# Enhanced Recommendation Function with Cast
    def recommend(movie):
        index = new_df[new_df['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommendations = []
        for i in distances[1:6]:
            movie_title = new_df.iloc[i[0]].title
            movie_overview_list = new_df.iloc[i[0]].overview
            movie_crew_list = new_df.iloc[i[0]].crew
            movie_cast_list = new_df.iloc[i[0]].cast

            # Clean the overview
            movie_overview = ' '.join(movie_overview_list) if isinstance(movie_overview_list, list) else movie_overview_list

            # Clean the crew (director, etc.)
            movie_crew = ' '.join(movie_crew_list) if isinstance(movie_crew_list, list) else movie_crew_list

            # Clean the cast - add comma after space between names
            if isinstance(movie_cast_list, list):
                movie_cast = ', '.join(movie_cast_list)  # Changed from ' ' to ', '
            else:
                movie_cast = movie_cast_list

            recommendations.append({
                "title": movie_title,
                "overview": movie_overview,
                "crew": movie_crew,
                "cast": movie_cast
            })

        return recommendations
    
    # Show Recommendations
    if st.button("🎯 Get Recommendations"):
        st.markdown("## 🔥 Top 5 Recommendations:")
        results = recommend(selected_movie)

        for rec in results:
            st.markdown(f"""
                <div class="recommend-card">
                    <div class="recommend-title">{rec['title']}</div>
                    <div class="overview">{rec['overview']}</div>
                    <div class="crew"><b>Directed by:</b> {rec['crew']}</div>
                    <div class="cast"><b>Starring:</b> {rec['cast']}</div>
                </div>
            """, unsafe_allow_html=True)

elif selected == "About":
    st.markdown("""
    <h2 style='color: #ffffff;'>ℹ️ About FLIXREC</h2>
    <p>FLIXREC is a smart movie recommendation engine that uses <b>content-based filtering</b> to suggest titles similar to your favorites. It analyzes features like overview, crew details, and keywords to understand and match patterns between movies.</p>

    <h4 style='margin-top: 1.5rem; color: #e50914;'>🧠 Technical Overview</h4>
    <ul style='line-height: 1.7;'>
        <li><b>Dataset</b>: TMDB 5000 Movies Dataset</li>
        <li><b>Algorithm</b>: Cosine Similarity for content-based filtering</li>
        <li><b>Analyzed Features</b>: Overview, Crew, Keywords, Genres</li>
    </ul>

    <h4 style='margin-top: 1.5rem; color: #e50914;'>🔮 Future Enhancements</h4>
    <ul style='line-height: 1.7;'>
        <li>Integrate collaborative filtering (user behavior based)</li>
        <li>Include real-time user ratings and reviews</li>
        <li>Build user profiles for personalized recommendations</li>
    </ul>
    """, unsafe_allow_html=True)