import streamlit as st
import pandas as pd
import time

# --- 1. UI CONFIGURATION & MIDNIGHT CYAN THEME ---
# We force the app to use the full width and open the sidebar by default
st.set_page_config(page_title="AI Recommender Pro", page_icon="🍿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Dark Midnight Theme Base */
    .stApp { 
        background-color: #0B0F19; 
        color: #E2E8F0; 
    }
    
    /* Neon Cyan Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 10px 30px -5px rgba(6, 182, 212, 0.4);
        margin-bottom: 40px;
    }
    .hero-banner h1 { color: #ffffff; margin: 0; font-weight: 900; font-family: 'Trebuchet MS', sans-serif; letter-spacing: 1px; text-transform: uppercase;}
    .hero-banner p { color: #cffafe; margin-top: 5px; font-size: 1.2rem; font-weight: 500;}
    
    /* Customizing the Native Container to look like Glass/Premium Cards */
    div[data-testid="stVerticalBlock"] div[style*="border"] {
        background-color: #111827; /* Darker Slate */
        border: 1px solid #1e293b !important;
        border-top: 4px solid #06b6d4 !important; /* Cyan Top Accent */
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        height: 100%;
    }
    div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(6, 182, 212, 0.15);
        border: 1px solid #06b6d4 !important;
        border-top: 4px solid #06b6d4 !important;
    }
    
    /* Adjusting text inside the cards */
    .movie-title { font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-bottom: 5px; margin-top: 10px;}
    .movie-rating { font-size: 1rem; color: #fbbf24; font-weight: bold;}
    .movie-tags { font-size: 0.85rem; color: #22d3ee; margin-bottom: 15px; font-style: italic;}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE MOCK API DATABASE ---
@st.cache_data
def fetch_movie_api_database():
    api_data = {
        'Title': [
            'The Dark Knight', 'Inception', 'The Notebook', 'Titanic', 
            'Interstellar', 'Avengers: Endgame', 'John Wick', 'La La Land', 
            'The Terminator', 'Gladiator', 'The Conjuring', 'Superbad'
        ],
        'Image_URL': [
            'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg',
            'https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/8/86/Posternotebook.jpg',
            'https://upload.wikimedia.org/wikipedia/en/1/18/Titanic_%281997_film%29_poster.png',
            'https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/9/98/John_Wick_TeaserPoster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/a/ab/La_La_Land_%28film%29.png',
            'https://upload.wikimedia.org/wikipedia/en/7/70/Terminator1984movieposter.jpg',
            'https://upload.wikimedia.org/wikipedia/en/f/fb/Gladiator_%282000_film_poster%29.png',
            'https://upload.wikimedia.org/wikipedia/en/1/1f/Conjuring_poster.jpg',
            'https://upload.wikimedia.org/wikipedia/en/8/8b/Superbad_Poster.png'
        ],
        'Genres': [
            ['Action', 'Crime', 'Drama', 'Thriller'],
            ['Action', 'Sci-Fi', 'Thriller'],
            ['Romance', 'Drama'],
            ['Romance', 'Drama'],
            ['Sci-Fi', 'Adventure', 'Drama'],
            ['Action', 'Sci-Fi', 'Adventure'],
            ['Action', 'Thriller'],
            ['Romance', 'Musical', 'Comedy'],
            ['Action', 'Sci-Fi'],
            ['Action', 'Adventure', 'Drama'],
            ['Horror', 'Thriller'],
            ['Comedy']
        ],
        'Rating': [9.0, 8.8, 7.8, 7.9, 8.6, 8.4, 7.4, 8.0, 8.1, 8.5, 7.5, 7.6],
        'Description': [
            "Batman faces the Joker in Gotham City.",
            "A thief enters the dreams of others to steal secrets.",
            "A poor man and a rich woman fall in love in the 1940s.",
            "Romance blossoms on the ill-fated R.M.S. Titanic.",
            "Explorers travel through a wormhole in space to save humanity.",
            "The Avengers assemble once more to reverse Thanos' snap.",
            "An ex-hitman comes out of retirement for vengeance.",
            "A jazz pianist and an actress fall in love.",
            "A cyborg is sent back in time to alter the future.",
            "A betrayed Roman General seeks revenge.",
            "Paranormal investigators help a family in terror.",
            "Two high school friends try to buy alcohol for a party."
        ]
    }
    return pd.DataFrame(api_data)

df = fetch_movie_api_database()
all_genres = sorted(list(set(genre for sublist in df['Genres'] for genre in sublist)))

# --- 3. THE SIDEBAR (UX REDESIGN) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1024px-Netflix_2015_logo.svg.png", width=150)
    st.markdown("---")
    st.markdown("### 🎛️ AI Engine Controls")
    
    selected_genres = st.multiselect(
        "🧠 Feed the AI your favorite genres:",
        options=all_genres,
        default=["Action", "Sci-Fi"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    min_rating = st.slider("⭐ Minimum Rating Quality:", 1.0, 10.0, 7.5, 0.5)
    
    st.markdown("---")
    st.success("✅ FUTO Wi-Fi Connection Stable")
    st.caption("Architect: Francis Ezeh C.")
    st.caption("Reg: [REG NO]")

# --- 4. MAIN DASHBOARD (GRID LAYOUT) ---
st.markdown("""
<div class="hero-banner">
    <h1>🍿 The Cinematic Nexus</h1>
    <p>AI-Powered Content Filtering API Simulation</p>
</div>
""", unsafe_allow_html=True)

if not selected_genres:
    st.warning("👈 Awaiting user input. Please configure the AI Engine in the sidebar.")
else:
    with st.spinner('Neural Network scanning database for exact matches...'):
        time.sleep(0.6) 
        
        # Filtering Math
        df['Match_Count'] = df['Genres'].apply(lambda x: len(set(x).intersection(set(selected_genres))))
        results = df[(df['Match_Count'] > 0) & (df['Rating'] >= min_rating)].copy()
        results = results.sort_values(by=['Match_Count', 'Rating'], ascending=[False, False])
        
        if results.empty:
            st.error("📡 AI Error: No titles match these strict parameters. Broaden your search in the sidebar.")
        else:
            st.markdown(f"### 🔥 Top {len(results)} Matches Found for You")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- THE MAGIC GRID UX ---
            # We create 3 columns. Streamlit will place movies side-by-side!
            num_cols = 3
            cols = st.columns(num_cols)
            
            for index, (i, row) in enumerate(results.iterrows()):
                # Determine which column this movie goes into (0, 1, or 2)
                col = cols[index % num_cols]
                
                with col:
                    with st.container(border=True):
                        # Native image filling the container width
                        st.image(row['Image_URL'], use_container_width=True)
                        
                        genres_str = " • ".join(row['Genres'])
                        st.markdown(f"""
                        <div class="movie-title">{row['Title']}</div>
                        <div class="movie-rating">⭐ {row['Rating']} </div>
                        <div class="movie-tags">{genres_str}</div>
                        """, unsafe_allow_html=True)
                        
                        st.write(row['Description'])
                        
                        # Show the AI logic (How many tags matched the user's request)
                        st.caption(f"🎯 AI Match Strength: {row['Match_Count']} Tags")