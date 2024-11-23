from flask import Flask, jsonify
import requests
import sqlite3
import pandas as pd
import ast
import time

app = Flask(__name__)


# @app.route('/tables')
# def get_tables_and_columns():
#     # Connect to your SQLite database
#     conn = sqlite3.connect('movies.db')
#     cursor = conn.cursor()

#     # Get all table names
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()

#     # Create a dictionary to store tables and their columns
#     tables_info = {}

#     # Loop through the tables and fetch their columns
#     for table in tables:
#         table_name = table[0]
#         cursor.execute(f"PRAGMA table_info({table_name});")
#         columns = cursor.fetchall()

#         # Add the table and its columns to the dictionary
#         tables_info[table_name] = [{"column_name": column[1], "data_type": column[2]} for column in columns]

#     # Close the connection
#     conn.close()

#     # Return the tables and columns as JSON
#     return jsonify(tables_info)

# API_KEY = 'ddfbd71a6d0caa560e3a1f793b91aa5f'
# BASE_URL = "https://api.themoviedb.org/3"

# def fetch_with_retry(url, params, retries=3, backoff_factor=1):
#     for attempt in range(retries):
#         try:
#             response = requests.get(url, params=params, timeout=10)  # Set a timeout
#             response.raise_for_status()  # Raise an error for HTTP codes >= 400
#             return response
#         except requests.exceptions.RequestException as e:
#             if attempt < retries - 1:
#                 wait = backoff_factor * (2 ** attempt)  # Exponential backoff
#                 print(f"Error: {e}. Retrying in {wait} seconds...")
#                 time.sleep(wait)
#             else:
#                 raise

# def fetch_movies(year_start, year_end, page=1):
#     url = f"{BASE_URL}/discover/movie"
#     params = {
#         "api_key": API_KEY,
#         "language": "en-US",
#         "sort_by": "vote_average.desc",
#         "primary_release_date.gte": f"{year_start}-01-01",
#         "primary_release_date.lte": f"{year_end}-12-31",
#         "vote_count.gte": 2000 if year_end <= 2022 else 500,
#         "vote_average.gte": 6,
#         "page": page
#     }
#     response = fetch_with_retry(url, params=params)
#     return response.json()

# def fetch_movie_details(movie_id):
#     url = f"{BASE_URL}/movie/{movie_id}"
#     params = {"api_key": API_KEY, "language": "en-US"}
#     response = fetch_with_retry(url, params=params)
#     return response.json()

# def fetch_credits(movie_id):
#     url = f"{BASE_URL}/movie/{movie_id}/credits"
#     params = {"api_key": API_KEY}
#     response = fetch_with_retry(url, params=params)
#     return response.json()

# def movie_exists(cursor, movie_id):
#     cursor.execute('SELECT 1 FROM Movies WHERE movie_id = ?', (movie_id,))
#     return cursor.fetchone() is not None

# def populate_movies(cursor, movie):
#     cursor.execute('''
#         INSERT OR IGNORE INTO Movies (
#             movie_id, title, original_title, budget, original_language,
#             release_date, revenue, runtime, overview, production_companies,
#             production_countries, rating_avg, rating_count, country,
#             backdrop_path, poster_path, adult
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (
#         movie['id'], movie['title'], movie['original_title'], movie.get('budget', 0),
#         movie['original_language'], movie['release_date'], movie.get('revenue', 0),
#         movie.get('runtime', 0), movie.get('overview', 'No Overview'),
#         ', '.join([c['name'] for c in movie.get('production_companies', [])]),
#         ', '.join([c['name'] for c in movie.get('production_countries', [])]),
#         movie['vote_average'], movie['vote_count'],
#         ', '.join([c['name'] for c in movie.get('production_countries', [])]),
#         movie.get('backdrop_path', 'Backdrop is not available'),
#         movie.get('poster_path', 'Poster is not available'),
#         movie['adult']
#     ))

# def populate_genres(cursor, movie):
#     for genre in movie.get('genres', []):
#         cursor.execute('''
#             INSERT OR IGNORE INTO Genres (genre_id, genre_name)
#             VALUES (?, ?)
#         ''', (genre['id'], genre['name']))
#         cursor.execute('''
#             INSERT OR IGNORE INTO Movies_Genres (movie_id, genre_id)
#             VALUES (?, ?)
#         ''', (movie['id'], genre['id']))

# def populate_actors_and_crew(cursor, credits, movie_id):
#     for cast in credits.get('cast', []):
#         cursor.execute('''
#             INSERT OR IGNORE INTO Actors (actor_id, actor_name, character_name)
#             VALUES (?, ?, ?)
#         ''', (cast['id'], cast['name'], cast.get('character', 'Unknown')))
#         cursor.execute('''
#             INSERT OR IGNORE INTO Movies_Actors (movie_id, actor_id)
#             VALUES (?, ?)
#         ''', (movie_id, cast['id']))
    
#     for crew in credits.get('crew', []):
#         if crew['job'] in ['Director', 'Producer', 'Writer']:
#             cursor.execute('''
#                 INSERT OR IGNORE INTO Crew (crew_id, crew_name, job_title)
#                 VALUES (?, ?, ?)
#             ''', (crew['id'], crew['name'], crew['job']))
#             cursor.execute('''
#                 INSERT OR IGNORE INTO Movies_Crew (movie_id, crew_id)
#                 VALUES (?, ?)
#             ''', (movie_id, crew['id']))

# def main():
#     conn = sqlite3.connect('movies.db')
#     cursor = conn.cursor()
    
#     total_movies_populated = 0
#     total_pages = 100  # You can increase or decrease this based on the desired movie count

#     for year_start, year_end in [(1970, 2024)]:
#         for page in range(51, total_pages + 1):  # Fetch multiple pages (250 pages for 5000+ movies)
#             movies = fetch_movies(year_start, year_end, page).get('results', [])
#             print(f"Fetched {len(movies)} movies for page {page} ({year_start}-{year_end}).")
#             for movie in movies:
#                 details = fetch_movie_details(movie['id'])
#                 credits = fetch_credits(movie['id'])
                
#                 # Populate tables only if the movie doesn't already exist
#                 if not movie_exists(cursor, movie['id']):
#                     populate_movies(cursor, details)
#                     populate_genres(cursor, details)
#                     populate_actors_and_crew(cursor, credits, movie['id'])
#                     total_movies_populated += 1
#                     print(f"Populated movie: {movie['title']} (ID: {movie['id']})")
#                 else:
#                     print(f"Skipping movie: {movie['title']} (ID: {movie['id']}) - already in the database.")

#     conn.commit()
#     conn.close()

#     print(f"Total movies populated: {total_movies_populated}")


# @app.route('/movie/<title>', methods=['GET'])
# def get_movie_details(title):
#     try:
#         conn = sqlite3.connect('movies.db')
#         cursor = conn.cursor()

#         # Query for the movie details
#         cursor.execute('''
#             SELECT movie_id, title, original_title, budget, original_language,
#                    release_date, revenue, runtime, overview, production_companies,
#                    production_countries, rating_avg, rating_count, country,
#                    backdrop_path, poster_path, adult
#             FROM Movies
#             WHERE title = ?
#         ''', (title,))
#         movie = cursor.fetchone()

#         if not movie:
#             return jsonify({"error": "Movie not found"}), 404

#         movie_details = {
#             "movie_id": movie[0],
#             "title": movie[1],
#             "original_title": movie[2],
#             "budget": movie[3],
#             "original_language": movie[4],
#             "release_date": movie[5],
#             "revenue": movie[6],
#             "runtime": movie[7],
#             "overview": movie[8],
#             "production_companies": movie[9],
#             "production_countries": movie[10],
#             "rating_avg": movie[11],
#             "rating_count": movie[12],
#             "country": movie[13],
#             "backdrop_path": movie[14],
#             "poster_path": movie[15],
#             "adult": bool(movie[16]),
#         }

#         # Query for genres
#         cursor.execute('''
#             SELECT g.genre_name
#             FROM Genres g
#             JOIN Movies_Genres mg ON g.genre_id = mg.genre_id
#             WHERE mg.movie_id = ?
#         ''', (movie[0],))
#         genres = [genre[0] for genre in cursor.fetchall()]

#         # Query for cast (actors)
#         cursor.execute('''
#             SELECT a.actor_name, a.character_name
#             FROM Actors a
#             JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
#             WHERE ma.movie_id = ?
#         ''', (movie[0],))
#         cast = [{"actor_name": actor[0], "character_name": actor[1]} for actor in cursor.fetchall()]

#         # Query for crew
#         cursor.execute('''
#             SELECT c.crew_name, c.job_title
#             FROM Crew c
#             JOIN Movies_Crew mc ON c.crew_id = mc.crew_id
#             WHERE mc.movie_id = ?
#         ''', (movie[0],))
#         crew = [{"crew_name": crew_member[0], "job_title": crew_member[1]} for crew_member in cursor.fetchall()]

#         conn.close()

#         # Combine all details
#         return jsonify({
#             "movie_details": movie_details,
#             "genres": genres,
#             "cast": cast,
#             "crew": crew
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/movies')
# def get_movies():
#     conn = sqlite3.connect('movies.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Movies;')
#     movies = cursor.fetchall()
#     conn.close()
#     return jsonify(movies)



@app.route('/movies')
def get_users():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Movies LIMIT 10;')
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)


# def main():
#     conn = sqlite3.connect('movies.db')
#     cursor = conn.cursor()

#     # Get the total number of movies in the database
#     conn = sqlite3.connect('movies.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT COUNT(*) FROM Movies')
#     total_movies = cursor.fetchone()[0]
#     print(f"Total number of movies in the database: {total_movies}")
#     conn.close()

@app.route('/')
def home():
    return 'Welcome to the Movies API!'

if __name__ == '__main__':
    #main()
    app.run(debug=True)
