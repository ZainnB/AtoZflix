from flask import Flask, jsonify
import sqlite3
import time
import requests

app = Flask(__name__)


# Create a connection to the SQLite database
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Create the Movies table using raw SQL
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movies(
                movie_id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                original_title VARCHAR(255) NOT NULL,
                budget BIGINT NOT NULL,
                original_language VARCHAR(10) NOT NULL,
                release_date DATE NOT NULL DEFAULT '0000-00-00',
                revenue BIGINT NOT NULL,
                runtime INT NOT NULL DEFAULT 0, 
                overview TEXT NOT NULL DEFAULT 'No Overview',
                production_companies TEXT NOT NULL,
                production_countries TEXT NOT NULL,
                rating_avg FLOAT NOT NULL CHECK(rating_avg >= 0 AND rating_avg <= 10),
                rating_count INT NOT NULL,          
                country VARCHAR(255) NOT NULL DEFAULT 'Unknown',
                backdrop_path VARCHAR(255) NOT NULL DEFAULT 'Backdrop is not available',
                poster_path VARCHAR(255) NOT NULL DEFAULT 'Poster is not available',
                adult BOOLEAN NOT NULL DEFAULT FALSE
            );
''')

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

# Create a new table Actors
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Actors (
                actor_id INTEGER PRIMARY KEY,
                actor_name VARCHAR(255) NOT NULL,
                character_name VARCHAR(255) NOT NULL
                )
''')


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

# Create a new table Crew
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Crew (
                crew_id INTEGER PRIMARY KEY,
                crew_name VARCHAR(255) NOT NULL,
                job_title VARCHAR(255) NOT NULL
            )
''')

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

#WatchHistory Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS WatchHistory (
                movie_id INT,
                user_id INT,
                watch_date DATE DEFAULT CURRENT_DATE,
                rating_id INT,
                PRIMARY KEY(movie_id, user_id),
                FOREIGN KEY(movie_id) REFERENCES Movies(movie_id),
                FOREIGN KEY(user_id) REFERENCES Users(user_id)
            )
''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS Favorites (
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                rating_id INT NOT NULL,
                added_at DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                FOREIGN KEY (rating_id) REFERENCES Ratings(rating_id),
                UNIQUE (user_id, movie_id)
            )
''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS To_Be_Watched (
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                added_at DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                UNIQUE (user_id, movie_id)
            )
''')


# Commit the changes and close the connection
conn.commit()
conn.close()

API_KEY = 'ddfbd71a6d0caa560e3a1f793b91aa5f'
BASE_URL = "https://api.themoviedb.org/3"

def fetch_with_retry(url, params, retries=3, backoff_factor=1):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)  # Set a timeout
            response.raise_for_status()  # Raise an error for HTTP codes >= 400
            return response
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                wait = backoff_factor * (2 ** attempt)  # Exponential backoff
                print(f"Error: {e}. Retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                raise

def fetch_movies(year_start, year_end, page=1):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "sort_by": "vote_average.desc",
        "primary_release_date.gte": f"{year_start}-01-01",
        "primary_release_date.lte": f"{year_end}-12-31",
        "vote_count.gte": 2000 if year_end <= 2022 else 500,
        "vote_average.gte": 6,
        "page": page
    }
    response = fetch_with_retry(url, params=params)
    return response.json()

def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = fetch_with_retry(url, params=params)
    return response.json()

def fetch_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {"api_key": API_KEY}
    response = fetch_with_retry(url, params=params)
    return response.json()

def movie_exists(cursor, movie_id):
    cursor.execute('SELECT 1 FROM Movies WHERE movie_id = ?', (movie_id,))
    return cursor.fetchone() is not None

def populate_movies(cursor, movie):
    cursor.execute('''
        INSERT OR IGNORE INTO Movies (
            movie_id, title, original_title, budget, original_language,
            release_date, revenue, runtime, overview, production_companies,
            production_countries, rating_avg, rating_count, country,
            backdrop_path, poster_path, adult
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        movie['id'], movie['title'], movie['original_title'], movie.get('budget', 0),
        movie['original_language'], movie['release_date'], movie.get('revenue', 0),
        movie.get('runtime', 0), movie.get('overview', 'No Overview'),
        ', '.join([c['name'] for c in movie.get('production_companies', [])]),
        ', '.join([c['name'] for c in movie.get('production_countries', [])]),
        movie['vote_average'], movie['vote_count'],
        ', '.join([c['name'] for c in movie.get('production_countries', [])]),
        movie.get('backdrop_path', 'Backdrop is not available'),
        movie.get('poster_path', 'Poster is not available'),
        movie['adult']
    ))

def populate_genres(cursor, movie):
    for genre in movie.get('genres', []):
        cursor.execute('''
            INSERT OR IGNORE INTO Genres (genre_id, genre_name)
            VALUES (?, ?)
        ''', (genre['id'], genre['name']))
        cursor.execute('''
            INSERT OR IGNORE INTO Movies_Genres (movie_id, genre_id)
            VALUES (?, ?)
        ''', (movie['id'], genre['id']))

def populate_actors_and_crew(cursor, credits, movie_id):
    for cast in credits.get('cast', []):
        cursor.execute('''
            INSERT OR IGNORE INTO Actors (actor_id, actor_name, character_name)
            VALUES (?, ?, ?)
        ''', (cast['id'], cast['name'], cast.get('character', 'Unknown')))
        cursor.execute('''
            INSERT OR IGNORE INTO Movies_Actors (movie_id, actor_id)
            VALUES (?, ?)
        ''', (movie_id, cast['id']))
    
    for crew in credits.get('crew', []):
        if crew['job'] in ['Director', 'Producer', 'Writer']:
            cursor.execute('''
                INSERT OR IGNORE INTO Crew (crew_id, crew_name, job_title)
                VALUES (?, ?, ?)
            ''', (crew['id'], crew['name'], crew['job']))
            cursor.execute('''
                INSERT OR IGNORE INTO Movies_Crew (movie_id, crew_id)
                VALUES (?, ?)
            ''', (movie_id, crew['id']))

def main():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    total_movies_populated = 0
    total_pages = 2  # You can increase or decrease this based on the desired movie count

    for year_start, year_end in [(1970, 2024)]:
        for page in range(1, total_pages + 1):  # Fetch multiple pages (250 pages for 5000+ movies)
            movies = fetch_movies(year_start, year_end, page).get('results', [])
            print(f"Fetched {len(movies)} movies for page {page} ({year_start}-{year_end}).")
            for movie in movies:
                details = fetch_movie_details(movie['id'])
                credits = fetch_credits(movie['id'])
                
                # Populate tables only if the movie doesn't already exist
                if not movie_exists(cursor, movie['id']):
                    populate_movies(cursor, details)
                    populate_genres(cursor, details)
                    populate_actors_and_crew(cursor, credits, movie['id'])
                    total_movies_populated += 1
                    print(f"Populated movie: {movie['title']} (ID: {movie['id']})")
                else:
                    print(f"Skipping movie: {movie['title']} (ID: {movie['id']}) - already in the database.")

    conn.commit()
    conn.close()

    print(f"Total movies populated: {total_movies_populated}")


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