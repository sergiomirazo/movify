import streamlit as st
import pandas as pd
import requests

# Download and load the dataset 
url = 'https://raw.githubusercontent.com/sergiomirazo/datasets/main/movies.csv'
response = requests.get(url)
with open('movies.csv', 'wb') as f:
    f.write(response.content)

# Read the dataset into a DataFrame
df = pd.read_csv("movies.csv", encoding="latin-1")

# Configure Streamlit
st.set_page_config(page_title="Movify", layout="wide")

# Main title of the app
st.title("Movify")

# Adding custom CSS
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #90ee90;
    }

    .stButton button:hover {
        background-color: #008000;
        color: white;
        border-color: #008000;
    }

    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar for different functionalities
st.sidebar.header("Control Panel")

st.sidebar.image("LOGO.png", caption="", width=150)

# Checkbox to show all movies
show_all = st.sidebar.checkbox("Show all movies")

if show_all:
    st.header("All movies")
    st.dataframe(df)

# Search movies by title
st.sidebar.subheader("Search movies by title")
search_title = st.sidebar.text_input("Movie title:")
if st.sidebar.button("Search movies"):
    filtered_df = df[df['name'].str.contains(search_title, case=False, na=False)]
    st.header(f"Total movies displayed: {len(filtered_df)}")
    st.dataframe(filtered_df)

# Select director to filter movies
st.sidebar.subheader("Select Director")
directors = df['director'].dropna().unique().tolist()
selected_director = st.sidebar.selectbox("Select Director", directors)
if st.sidebar.button("Filter director"):
    director_filtered_df = df[df['director'] == selected_director]
    st.header(f"Total movies found: {len(director_filtered_df)}")
    st.dataframe(director_filtered_df)

# Form to insert a new movie
st.sidebar.subheader("New movie")
new_name = st.sidebar.text_input("Movie name")
new_company = st.sidebar.text_input("Company")
if st.sidebar.button("Add movie"):
    new_data = {'name': new_name, 'company': new_company}
    df = df.append(new_data, ignore_index=True)
    st.success("New movie successfully added!")

# Save the updated DataFrame as a CSV file (if applicable)
df.to_csv('movies_updated.csv', index=False)