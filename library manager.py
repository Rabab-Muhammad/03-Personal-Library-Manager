import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime 
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Page Config
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie animation from URL
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Inject custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color : #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
     }

    .sub-header {
        font-size: 1.8rem !important;
        color : #3B82F6;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .success-msg {
        padding: 1rem;
        background-color : #ECFDF5;
        border-left: 5px solid #10B981;
        border-radius : 0.375rem;
    }

    .warning-msg {
        padding: 1rem;
        background-color : #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 0.375rem;
    }

    .book-card {
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
        transition: transform 0.3s ease;
    }

    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }

    .read-badge {
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius : 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .unread-badge {
         background-color: #F87171;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius : 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .action-button {
        margin-right: 0.5rem;
    }

    .stButton>button {
        border-radius : 0.375rem;
    }

    .sidebar-animation {
        margin-bottom: 1rem;
        padding: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Animation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-size:1.5rem;'>📘 Library Menu</h2>", unsafe_allow_html=True)

    # Load animated book icon
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_myejiggj.json"  
    lottie_data = load_lottieurl(lottie_url)
    if lottie_data:
        st_lottie(lottie_data, height=150, key="book_icon")

# Session state setup
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

# Load & Save Library
def load_library():
    if os.path.exists('library.json'):
        with open('library.json', 'r') as f:
            st.session_state.library = json.load(f)

def save_library():
    with open('library.json', 'w') as f:
        json.dump(st.session_state.library, f)

# Add, Remove, Search
def add_book(title, author, year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        st.session_state.library.pop(index)
        save_library()
        st.session_state.book_removed = True

def search_book(term, by):
    term = term.lower()
    st.session_state.search_results = [book for book in st.session_state.library if term in book[by].lower()]

# Statistics
def get_library_stats():
    total = len(st.session_state.library)
    read = sum(1 for b in st.session_state.library if b['read_status'])
    genres, authors, decades = {}, {}, {}

    for b in st.session_state.library:
        genres[b['genre']] = genres.get(b['genre'], 0) + 1
        authors[b['author']] = authors.get(b['author'], 0) + 1
        decade = (b['publication_year'] // 10) * 10
        decades[decade] = decades.get(decade, 0) + 1

    return {
        'total_books': total,
        'read_books': read,
        'percent_read': round((read / total) * 100, 2) if total > 0 else 0,
        'genres': genres,
        'authors': authors,
        'decades': decades
    }

def create_visualizations(stats):
    if stats['total_books'] > 0:
        fig_read = go.Figure(data=[go.Pie(
            labels=["Read", "Unread"],
            values=[stats['read_books'], stats['total_books'] - stats['read_books']],
            hole=0.4,
            marker_colors=["#10B981", "#F87171"]
        )])
        fig_read.update_layout(title="Read vs Unread Books")
        st.plotly_chart(fig_read, use_container_width=True)

    if stats['genres']:
        df = pd.DataFrame({'Genre': list(stats['genres'].keys()), 'Count': list(stats['genres'].values())})
        fig = px.bar(df, x="Genre", y="Count", color="Count", color_continuous_scale="Blues")
        fig.update_layout(title="Books by Genre")
        st.plotly_chart(fig, use_container_width=True)

    if stats['decades']:
        df = pd.DataFrame({'Decade': [f"{d}s" for d in stats['decades']], 'Count': list(stats['decades'].values())})
        fig = px.line(df, x="Decade", y="Count", markers=True)
        fig.update_layout(title="Books by Decade")
        st.plotly_chart(fig, use_container_width=True)

# Load library
load_library()

# Sidebar Navigation
nav = st.sidebar.radio("Navigate", ["View Library", "Add Book", "Search Books", "Library Statistics"])
st.session_state.current_view = nav.lower().replace(" ", "_")

# Main Title
st.markdown("<h1 class='main-header'>📖 Personal Library Manager</h1>", unsafe_allow_html=True)

# Views
if st.session_state.current_view == "add_book":
    st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Year", min_value=1000, max_value=datetime.now().year, value=2023)
        with col2:
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Tech", "Fantasy", "History", "Other"])
            status = st.radio("Status", ["Read", "Unread"], horizontal=True)
        submit = st.form_submit_button("Add Book")
        if submit and title and author:
            add_book(title, author, year, genre, status == "Read")
    if st.session_state.book_added:
        st.markdown("<div class='success-msg'>✅ Book Added!</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.book_added = False

elif st.session_state.current_view == "view_library":
    st.markdown("<h2 class='sub-header'>📚 Your Library</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.markdown("<div class='warning-msg'>⚠️ No books found.</div>", unsafe_allow_html=True)
    else:
        for idx, book in enumerate(st.session_state.library):
            badge_class = "read-badge" if book['read_status'] else "unread-badge"
            badge_text = "Read" if book['read_status'] else "Unread"
            book_html = f"""
            <div class='book-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong>{book['title']}</strong><br>
                        <em>by {book['author']}</em><br>
                       <span>{book.get('publication_year', 'N/A')} • {book.get('genre', 'N/A')}</span>
                    </div>
                    <div>
                        <span class='{badge_class}'>{badge_text}</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(book_html, unsafe_allow_html=True)
            st.button("🗑️ Remove", key=f"rm_{idx}", on_click=remove_book, args=(idx,))

elif st.session_state.current_view == "search_books":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True)
    term = st.text_input("Enter search term")
    by = st.selectbox("Search by", ["title", "author", "genre"])
    if term:
        search_book(term, by)
        if st.session_state.search_results:
            for b in st.session_state.search_results:
                st.markdown(f"**{b['title']}** by {b['author']} ({b['publication_year']}) - {b['genre']} | {'✅ Read' if b['read_status'] else '❌ Unread'}")
        else:
            st.warning("No results found.")

elif st.session_state.current_view == "library_statistics":
    st.markdown("<h2 class='sub-header'>📊 Library Statistics</h2>", unsafe_allow_html=True)
    stats = get_library_stats()
    st.write(f"**Total Books:** {stats['total_books']} | **Read:** {stats['read_books']} | **% Read:** {stats['percent_read']}%")
    create_visualizations(stats)
