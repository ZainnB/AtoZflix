from flask import Flask, jsonify
import sqlite3
import pandas as pd
import json
import ast
import requests

app = Flask(__name__)

# Loading the datasets
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

# Merging the datasets on 'id'
merged_data = pd.merge(movies, credits, left_on='id', right_on='movie_id', suffixes=('_movie', '_credit'))

# Function to extract relevant cast fields
def extract_cast_data(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 10:
            L.append({
                'id': i['id'],
                'name': i['name'],
                'character': i['character']
            })
            counter += 1
        else:
            break
    return L

# Function to extract relevant crew fields
def my_fetch_crew(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director' or i['job']=='Writer' or i['job']=='Producer':
            L.append({
                'id': i['id'],
                'name': i['name'],
                'job': i['job']
            })
    return L

# Function to convert the 'keywords' column to a list of dictionaries
def convert1(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# Function to convert the 'genres' column to a list of dictionaries
def convert_genres(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append({
            'id': i['id'],
            'name': i['name']
        })
    return L


# Apply the function to the 'cast' column
merged_data['cast'] = merged_data['cast'].apply(extract_cast_data)
# Apply the function to the 'crew' column
merged_data['crew'] = merged_data['crew'].apply(my_fetch_crew)
# Apply the function to the 'keywords' column
merged_data['keywords'] = merged_data['keywords'].apply(convert1)
# Apply the function to the 'genres' column
merged_data['genres'] = merged_data['genres'].apply(convert_genres)

merged_data['production_companies'] = merged_data['production_companies'].apply(convert1)
merged_data['production_countries'] = merged_data['production_countries'].apply(convert1)

merged_data = merged_data.drop(['spoken_languages', 'title_credit', 'id', 'title_movie'], axis=1)

# Create a connection to the SQLite database
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Create the Movies table using raw SQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Movies(
        movie_id INT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        budget BIGINT NOT NULL,
        homepage VARCHAR(255),
        keywords TEXT NOT NULL,
        original_language VARCHAR(10) NOT NULL,
        release_date DATE NOT NULL DEFAULT '0000-00-00',
        revenue BIGINT NOT NULL,
        runtime INT NOT NULL DEFAULT 0, 
        status VARCHAR(50) NOT NULL DEFAULT 'Released' CHECK(status IN ('Released', 'Rumored', 'Post Production', 'In Production', 'Planned', 'Canceled')),
        tagline TEXT NOT NULL DEFAULT 'No Tagline',
        overview TEXT NOT NULL DEFAULT 'No Overview',
        production_companies TEXT NOT NULL,
        production_countries TEXT NOT NULL,
        rating_avg FLOAT NOT NULL CHECK(rating_avg >= 0 AND rating_avg <= 10),
        rating_count INT NOT NULL          
    );
''')

# Insert the data into the Movies table
for index, row in merged_data.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO Movies (movie_id, title, budget, homepage, keywords, 
                            original_language, release_date, revenue, runtime, 
                            status, tagline, overview, production_companies, 
                            production_countries, rating_avg, rating_count)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
    ''', (row['movie_id'], row['original_title'], row['budget'], row['homepage'], str(row['keywords']),
          row['original_language'], row['release_date'], row['revenue'], row['runtime'], row['status'],
          row['tagline'], row['overview'], str(row['production_companies']), str(row['production_countries']),
          row['vote_average'], row['vote_count']))
    

conn.commit()

cursor.execute('''
                CREATE TABLE IF NOT EXISTS Genres(
                    genre_id INT PRIMARY KEY,
                    genre_name VARCHAR(255) NOT NULL UNIQUE
                )
            ''')

# Create a new table Movies_Genres
cursor.execute('''
                CREATE TABLE IF NOT EXISTS Movies_Genres(
                    movie_id INT,
                    genre_id INT,
                    PRIMARY KEY (movie_id, genre_id),
                    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
                )
            ''')

# Populate the Genres table
for index, row in merged_data.iterrows():
    for genre in row['genres']:
        cursor.execute('''
            INSERT OR IGNORE INTO Genres (genre_id, genre_name)
            VALUES (?, ?)
        ''', (genre['id'], genre['name']))

#populate the Movies_Genres table
for index, row in merged_data.iterrows():
    for genre in row['genres']:
        cursor.execute('''
            INSERT OR IGNORE INTO Movies_Genres (movie_id, genre_id)
            VALUES (?, ?)
        ''', (row['movie_id'], genre['id']))

# Create a new table Actors
cursor.execute('''
CREATE TABLE IF NOT EXISTS Actors (
    actor_id INTEGER PRIMARY KEY,
    actor_name VARCHAR(255) NOT NULL,
    character_name VARCHAR(255) NOT NULL
    )
''')

#populating the Actors table
for index, row in merged_data.iterrows():
    for actor in row['cast']:
        cursor.execute('''
        INSERT OR IGNORE INTO Actors (actor_id, actor_name, character_name)
        VALUES (?, ?, ?)
        ''', (actor['id'], actor['name'], actor['character']))

# Create a new table Movies_Actors
cursor.execute('''
CREATE TABLE IF NOT EXISTS Movies_Actors (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY (movie_id, actor_id)
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES Actors(actor_id)
    )
''')

#populating the Movies_Actors table
for index, row in merged_data.iterrows():
    for actor in row['cast']:
        cursor.execute('''
        INSERT OR IGNORE INTO Movies_Actors (movie_id, actor_id)
        VALUES (?, ?)
        ''', (row['movie_id'], actor['id']))

# Create a new table Crew
cursor.execute('''
CREATE TABLE IF NOT EXISTS Crew (
    crew_id INTEGER PRIMARY KEY,
    crew_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL
)
''')

#populating the Crew table
for index, row in merged_data.iterrows():
    for crew in row['crew']:
        cursor.execute('''
        INSERT OR IGNORE INTO Crew (crew_id, crew_name, job_title)
        VALUES (?, ?, ?)
        ''', (crew['id'], crew['name'], crew['job']))

# Create a new table Movies_Crew
cursor.execute('''
CREATE TABLE IF NOT EXISTS Movies_Crew (
    movie_id INT,
    crew_id INT,
    PRIMARY KEY (movie_id, crew_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
    FOREIGN KEY (crew_id) REFERENCES Crew(crew_id)
    )
''')

#populating the Movies_Crew table
for index, row in merged_data.iterrows():
    for crew in row['crew']:
        cursor.execute('''
        INSERT OR IGNORE INTO Movies_Crew (movie_id, crew_id)
        VALUES (?, ?)
        ''', (row['movie_id'], crew['id']))

#user Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE CHECK(email LIKE '%_@__%.__%'),
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
);
''')


#Ratings Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ratings (
                rating_id INT PRIMARY KEY,
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                rating INT NOT NULL CHECK(rating >= 0 AND rating <= 10),
                review TEXT,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);
''')

#Watchlist Table
cursor.execute("""
               CREATE TABLE Watchlist(
               movie_id INT,
               user_id INT,
                PRIMARY KEY(movie_id, user_id),
                FOREIGN KEY(movie_id) REFERENCES Movies(movie_id),
                FOREIGN KEY(user_id) REFERENCES Users(user_id)
                )
                """)


# Commit the changes and close the connection
conn.commit()
conn.close()


api_key = 'your_api_key_here'

def fetch_movie_poster(movie_title):
    """Fetch movie poster URL from TMDb API based on movie title."""
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_poster_url
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return None


def update_posters_for_movies():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    # Fetch titles starting from the specific title
    cursor.execute('''
        SELECT title FROM Movies
        WHERE Poster_URL = 'Poster is not available'
    ''')
    
    movies_to_update = cursor.fetchall()
    
    # Update poster URLs for the fetched movies
    for movie in movies_to_update:
        title = movie[0]
        poster_url = fetch_movie_poster(title)
        
        if poster_url:  # Only update if a valid poster URL is returned
            cursor.execute('''
                UPDATE Movies
                SET Poster_URL = ?
                WHERE title = ?;
            ''', (poster_url, title))
            print(f"Updated poster for: {title}")
            conn.commit()
        else:
            print(f"Poster not found for: {title}")

    
    conn.close()   # Close the connection


@app.route('/')
def home():
    return 'Welcome to the Movies API!'

@app.route('/movies')
def crew():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Movies LIMIT 10;')
    genres = cursor.fetchall()
    conn.close()
    return jsonify(genres)

if __name__ == '__main__':
    app.run(debug=True)