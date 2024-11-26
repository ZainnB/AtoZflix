from flask import Flask, jsonify, request
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
def get_movies():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users;')  # Adjust the query as needed
    movies = cursor.fetchall()
    conn.close()

    # Convert list of tuples to a list of dictionaries
    columns = [description[0] for description in cursor.description]
    movies_list = [dict(zip(columns, row)) for row in movies]

    return jsonify(movies_list)


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
