from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import re
import bcrypt
import json

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to validate email format
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# Registration POST API logic
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({"message": "All fields are required"}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format"}), 400

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({"message": "Email already registered"}), 400

        # Insert the new user with the plain password
        cursor.execute(
            "INSERT INTO Users (email, username, password) VALUES (?, ?, ?)",
            (email, username, password)  # Store the password directly
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route('/api/signin', methods=['POST'])
def signin():
    print("Headers:", request.headers)
    print("Body:", request.data)  # Raw body as bytes
    print("JSON Body:", request.get_json(silent=True))  # Attempt to parse JSON

    # Force JSON parsing if Content-Type is missing
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({"message": f"Invalid JSON: {str(e)}"}), 400

    input_data = data.get("username")  # Can be username or email
    password = data.get("password")

    # Determine if the input is an email or username
    if is_valid_email(input_data):
        query = "SELECT * FROM Users WHERE email = ?"
    else:
        query = "SELECT * FROM Users WHERE username = ?"

    # Fetch user record from the database
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access
    user = conn.execute(query, (input_data,)).fetchone()
    conn.close()

    if user:
        print("Fetched User:", dict(user))  # Debug: Print user data
    else:
        print("No user found")

    # Validate the user credentials
    if user and user['password'] == password:
        return jsonify({"user_id": user["user_id"], "success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

def calculate_trending(limit):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    query = """
            SELECT 
        M.title, 
        M.backdrop_path, 
        M.overview, 
        M.rating_avg, 
        M.runtime, 
        M.release_date,
        M.movie_id, 
        GROUP_CONCAT(G.genre_name, ', ') AS genres
        FROM Movies M
        LEFT JOIN Movies_Genres MG ON M.movie_id = MG.movie_id
        LEFT JOIN Genres G ON MG.genre_id = G.genre_id
        WHERE M.release_date >= DATE('now', '-6 months') 
        GROUP BY M.movie_id
        ORDER BY 
            (M.rating_avg * 0.7) + 
            (M.rating_count * 0.3) DESC 
        LIMIT ?;
"""


    cursor.execute(query, (limit,))
    movies = cursor.fetchall()
    conn.close()

    return [
        {
            "title": movie[0],
            "backdrop_path": movie[1],
            "overview": movie[2],
            "rating": movie[3],
            "duration": movie[4],
            "release_date": movie[5],
            "genres": movie[6],
            "movie_id": movie[7]
        }
        for movie in movies
    ]

@app.route('/api/trending', methods=['GET'])
def get_trending_movies():
    # Get limit from query parameters or default to 5
    limit = request.args.get('limit', default=5, type=int)
    
    try:
        movies = calculate_trending(limit)
        return jsonify({"status": "success", "movies": movies}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

# @app.route("/api/latest", methods=["GET"])
# def latest_movies():
#     limit = request.args.get("limit", default=10, type=int)
#     conn = sqlite3.connect('movies.db')  
#     cursor = conn.cursor()
#     # Query to fetch the latest movies
#     query = """
#     SELECT m.poster_path, m.movie_id
#     FROM Movies m
#     ORDER BY m.release_date DESC
#     LIMIT ?
#     """
    
#     try:
#         # Execute query with limit
#         cursor.execute(query, (limit,))
#         movies = cursor.fetchall()
#         conn.close()
#         formatted_movies = [
#             {"poster_path": movie[0],
#              "movie_id" : movie[1]
#             } for movie in movies
#         ]
#         return jsonify({"movies": formatted_movies}), 200
    
#     except Exception as e:
#         print(f"Error fetching latest movies: {e}")
#         return jsonify({"error": "Failed to fetch latest movies"}), 500
    
@app.route("/api/latest", methods=["GET"])
def latest_movies():
    limit = request.args.get("limit", default=80, type=int)  # Default to 80 movies per page
    offset = request.args.get("offset", default=0, type=int)  # Offset for pagination
    conn = sqlite3.connect('movies.db')  
    cursor = conn.cursor()
    query = """
    SELECT m.poster_path, m.movie_id
    FROM Movies m
    ORDER BY m.release_date DESC
    LIMIT ? OFFSET ?
    """
    
    try:
        cursor.execute(query, (limit, offset))
        movies = cursor.fetchall()
        conn.close()
        formatted_movies = [
            {"poster_path": movie[0],
             "movie_id": movie[1]
            } for movie in movies
        ]
        return jsonify({"movies": formatted_movies}), 200
    
    except Exception as e:
        print(f"Error fetching latest movies: {e}")
        return jsonify({"error": "Failed to fetch latest movies"}), 500

@app.route("/api/top_rated", methods=["GET"])
def top_rated_movies():
    limit = request.args.get("limit", default=10, type=int)
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    # Query to fetch top rated movies
    query = """
    SELECT m.poster_path, m.movie_id
    FROM Movies m
    ORDER BY m.rating_avg DESC
    LIMIT ?
    """
    
    try:
        # Execute query with limit
        cursor.execute(query, (limit,))
        movies = cursor.fetchall()
        conn.close()
        formatted_movies = [
            {"poster_path": movie[0],
              "movie_id" : movie[1]
            } for movie in movies
            ]
        return jsonify({"movies": formatted_movies}), 200
    
    except Exception as e:
        print(f"Error fetching top rated movies: {e}")
        return jsonify({"error": "Failed to fetch top rated movies"}), 500
    
@app.route('/api/get_genre_names')
def get_all_genre():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT DISTINCT genre_name FROM Genres"""
    try:
        cursor.execute(query)
        genres = cursor.fetchall()
        
        # Flatten the list of tuples to a list of strings
        genre_names = [genre[0] for genre in genres]
        
        return jsonify({"genres": genre_names}), 200
    except Exception as e:
        print(f"Error fetching genre details: {e}")
        return jsonify({"error": "Failed to fetch genre details"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/genre", methods=["GET"])
def genre_movies():
    genre = request.args.get("genre", type=str)
    limit = request.args.get("limit", default=10, type=int)
    
    # Fetch the genre_id from the genres table
    query = """
    SELECT g.genre_id
    FROM Genres g
    WHERE g.genre_name = ?
    """

    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute(query, (genre,))
    genre_id = cursor.fetchone()
    
    if genre_id:
        # Now fetch movies for the given genre_id
        query = """
        SELECT m.poster_path, m.movie_id
        FROM Movies m
        JOIN Movies_Genres mg ON m.movie_id = mg.movie_id
        WHERE mg.genre_id = ?
        LIMIT ?
        """
        try:
            cursor.execute(query, (genre_id[0], limit))
            movies = cursor.fetchall()
            conn.close()
            formatted_movies = [
                {"poster_path": movie[0],
                 "movie_id" : movie[1]
                } for movie in movies
            ]
            return jsonify({"movies": formatted_movies}), 200
        except Exception as e:
            print(f"Error fetching genre movies: {e}")
            return jsonify({"error": "Failed to fetch genre movies"}), 500
    else:
        return jsonify({"error": "Genre not found"}), 404


@app.route("/api/get_country_names", methods=["GET"])
def get_all_countries():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    query = """SELECT DISTINCT country FROM Movies"""
    try:
        cursor.execute(query)
        # Fetch all distinct country names
        countries = [row[0] for row in cursor.fetchall()]
        return jsonify({"countries": countries}), 200
    except Exception as e:
        print(f"Error fetching country details: {e}")
        return jsonify({"error": "Failed to fetch country details"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/country", methods=["GET"])
def country_movies():
    country = request.args.get("country", type=str)
    limit = request.args.get("limit", default=10, type=int)
    
    # Fetch movies for the given country
    query = """
    SELECT m.poster_path, m.movie_id
    FROM Movies m
    WHERE m.country = ?
    LIMIT ?
    """
    
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (country, limit))
        movies = cursor.fetchall()
        conn.close()
        formatted_movies = [
            {"poster_path": movie[0],
             "movie_id" : movie[1]
            } for movie in movies
        ]
        return jsonify({"movies": formatted_movies}), 200
    except Exception as e:
        print(f"Error fetching country movies: {e}")
        return jsonify({"error": "Failed to fetch country movies"}), 500

@app.route("/api/search_movie", methods=["GET"])
def search_movies():
    # Extract parameters from the request
    search_query = request.args.get("query", type=str)
    limit = request.args.get("limit", default=10, type=int)

    # Database connection
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row  # Allow dict-style access to rows
    cursor = conn.cursor()

    # SQL query to search for movies
    sql_query = """
    SELECT m.poster_path, m.movie_id
    FROM Movies m
    WHERE m.title LIKE ? COLLATE NOCASE
    LIMIT ?
    """

    try:
        # Execute the query with the correct parameters
        cursor.execute(sql_query, (f"%{search_query}%", limit))
        movies = cursor.fetchall()
        conn.close()

        # Format the fetched results
        formatted_movies = [{"poster_path": movie["poster_path"],
                             "movie_id": movie["movie_id"]
                            } for movie in movies]

        return jsonify({"movies": formatted_movies}), 200

    except Exception as e:
        # Handle any errors and return an error response
        conn.close()
        print(f"Error fetching search movies: {e}")
        return jsonify({"error": "Failed to fetch search movies"}), 500
    
@app.route("/api/search_actor", methods=["GET"])
def search_actors():
    # Extract parameters from the request
    actor_id = request.args.get("actor_id", type=int)
    search_query = request.args.get("query", type=str)
    limit = request.args.get("limit", default=10, type=int)

    # Database connection
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # If actor_id is provided, fetch the actor's name
        if actor_id:
            actor_query = "SELECT actor_name FROM Actors WHERE actor_id = ?"
            cursor.execute(actor_query, (actor_id,))
            actor = cursor.fetchone()

            if not actor:
                conn.close()
                return jsonify({"movies": [], "message": "Actor not found"}), 404

            # Use the actor's name as the search query
            search_query = actor["actor_name"]

        # SQL query to search for actors by name
        sql_query = """
        SELECT a.actor_id, a.actor_name
        FROM Actors a
        WHERE a.actor_name LIKE ? COLLATE NOCASE
        LIMIT ?
        """
        cursor.execute(sql_query, (f"%{search_query}%", limit))
        actors = cursor.fetchall()

        if not actors:
            conn.close()
            return jsonify({"movies": [], "message": "No actors found"}), 404

        actor_ids = [actor["actor_id"] for actor in actors]

        # Fetch movies for the found actors
        movie_query = """
        SELECT DISTINCT m.poster_path, m.movie_id
        FROM Movies m
        INNER JOIN Movies_Actors ma ON m.movie_id = ma.movie_id
        WHERE ma.actor_id IN ({});
        """.format(",".join(["?"] * len(actor_ids)))
        
        cursor.execute(movie_query, actor_ids)
        movies = cursor.fetchall()
        conn.close()

        # Format the results
        formatted_movies = [{"poster_path": movie["poster_path"], "movie_id": movie["movie_id"]} for movie in movies]

        return jsonify({"movies": formatted_movies}), 200

    except Exception as e:
        conn.close()
        print(f"Error fetching actor movies: {e}")
        return jsonify({"error": "Failed to fetch actor movies"}), 500


@app.route("/api/search_crew", methods=["GET"])
def search_crew():
    # Extract parameters from the request
    search_query = request.args.get("query", type=str)
    crew_id = request.args.get("crew_id", type=int)  # Allow search by crew_id
    limit = request.args.get("limit", default=10, type=int)

    # Database connection
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row  # Allow dict-style access to rows
    cursor = conn.cursor()

    try:
        # If crew_id is provided, find the crew name and update the search query
        if crew_id:
            crew_query = "SELECT crew_name FROM Crew WHERE crew_id = ?"
            cursor.execute(crew_query, (crew_id,))
            crew = cursor.fetchone()

            if not crew:
                conn.close()
                return jsonify({"movies": [], "message": "Crew member not found"}), 404

            # Use the crew's name as the search query
            search_query = crew["crew_name"]

        # If no search query is available at this point, return an error
        if not search_query:
            conn.close()
            return jsonify({"error": "No valid parameters provided"}), 400

        # Search for crew members by name
        sql_query = """
        SELECT c.crew_id, c.crew_name
        FROM Crew c
        WHERE c.crew_name LIKE ? COLLATE NOCASE
        LIMIT ?
        """
        cursor.execute(sql_query, (f"%{search_query}%", limit))
        crew = cursor.fetchall()

        if not crew:
            conn.close()
            return jsonify({"movies": [], "message": "No crew members found"}), 404

        crew_ids = [c["crew_id"] for c in crew]

        # Fetch movies for the found crew members
        movie_query = """
        SELECT DISTINCT m.poster_path, m.movie_id
        FROM Movies m
        INNER JOIN Movies_Crew mc ON m.movie_id = mc.movie_id
        WHERE mc.crew_id IN ({})
        """.format(",".join(["?"] * len(crew_ids)))

        cursor.execute(movie_query, crew_ids)
        movies = cursor.fetchall()
        conn.close()

        # Format the results
        formatted_movies = [{"poster_path": movie["poster_path"], "movie_id": movie["movie_id"]} for movie in movies]

        return jsonify({"movies": formatted_movies}), 200

    except Exception as e:
        conn.close()
        print(f"Error fetching crew movies: {e}")
        return jsonify({"error": "Failed to fetch crew movies"}), 500

    except Exception as e:
        conn.close()
        print(f"Error fetching crew movies: {e}")
        return jsonify({"error": "Failed to fetch crew movies"}), 500


@app.route('/api/top-actors', methods=['GET'])
def get_top_actors():
    try:
        # Get the limit parameter (default: 5)
        limit = int(request.args.get('limit', 5))
        
        # SQLite query to fetch top-rated actor IDs and names
        query = """
        WITH ActorRatings AS (
            SELECT
                a.actor_id,
                a.actor_name AS actor_name,
                SUM(m.rating_avg) AS total_rating
            FROM
                Actors a
            JOIN Movies_Actors ma ON a.actor_id = ma.actor_id
            JOIN Movies m ON ma.movie_id = m.movie_id
            GROUP BY a.actor_id
        )
        SELECT
            actor_id,
            actor_name
        FROM
            ActorRatings
        ORDER BY total_rating DESC
        LIMIT ?;
        """
        
        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the query with the limit parameter
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        conn.close()
        
        # Format response as list of dictionaries containing actor_id and actor_name
        actors = [{"actor_id": actor_id, "actor_name": actor_name} for (actor_id, actor_name) in results]
        
        return jsonify({"status": "success", "data": actors}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/actor-movies', methods=['GET'])
def get_actor_movies():
    try:
        # Get the actor_id and limit parameters from request
        actor_id = request.args.get('actor_id')  # Actor ID as a parameter
        limit = int(request.args.get('limit', 5))  # Default limit is 5

        # Check if actor_id is provided
        if not actor_id:
            return jsonify({"status": "error", "message": "actor_id parameter is required"}), 400

        query = """
        SELECT
            m.poster_path,
            m.movie_id
        FROM
            Movies m
        JOIN Movies_Actors ma ON m.movie_id = ma.movie_id
        WHERE
            ma.actor_id = ?
        ORDER BY
            m.rating_avg DESC
        LIMIT ?;
        """
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, (actor_id, limit))
        results = cursor.fetchall()
        
        conn.close()

        movies = []
        for poster_path, movie_id in results:
            movies.append({
                "poster_path": poster_path,
                "movie_id": movie_id
            })

        return jsonify({"status": "success", "data": movies}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/top-crew', methods=['GET'])
def get_top_crew():
    try:
        limit = int(request.args.get('limit', 5))
        
        # SQLite query to fetch top-rated crew IDs and names
        query = """
        WITH CrewRatings AS (
            SELECT
                c.crew_id,
                c.crew_name AS crew_name,
                c.job_title AS job_title,
                SUM(m.rating_avg) AS total_rating
            FROM
                Crew c
            JOIN Movies_Crew mc ON c.crew_id = mc.crew_id
            JOIN Movies m ON mc.movie_id = m.movie_id
            GROUP BY c.crew_id
        )
        SELECT
            crew_id,
            crew_name,
            job_title
        FROM
            CrewRatings
        ORDER BY total_rating DESC
        LIMIT ?;
        """
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        conn.close()
        
        crew = [{"crew_id": crew_id, "crew_name": crew_name, "job_title": job_title} for (crew_id, crew_name, job_title) in results]
        
        return jsonify({"status": "success", "data": crew}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/crew-movies', methods=['GET'])
def get_crew_movies():
    try:
        crew_id = request.args.get('crew_id')
        limit = int(request.args.get('limit', 5))

        if not crew_id:
            return jsonify({"status": "error", "message": "crew_id parameter is required"}), 400

        query = """
        SELECT
            m.poster_path,
            m.movie_id
        FROM
            Movies m
        JOIN Movies_Crew mc ON m.movie_id = mc.movie_id
        WHERE
            mc.crew_id = ?
        ORDER BY
            m.rating_avg DESC
        LIMIT ?;
        """
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, (crew_id, limit))
        results = cursor.fetchall()
        
        conn.close()

        movies = []
        for poster_path, movie_id in results:
            movies.append({
                "poster_path": poster_path,
                "movie_id": movie_id
            })

        return jsonify({"status": "success", "data": movies}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/movie_details", methods=["GET"])
def movie_details():
    movie_id = request.args.get("movie_id", type=int)
    
    # Fetch movie details for the given movie_id
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    query = """
    SELECT m.title, m.original_title, m.release_date, m.budget, m.revenue, m.runtime, m.overview, m.production_companies, 
           m.production_countries, m.rating_avg, m.rating_count, m.country, m.poster_path, m.backdrop_path, m.adult 
    FROM Movies m
    WHERE m.movie_id = ?
    """

    try:
        cursor.execute(query, (movie_id,))
        movie = cursor.fetchone()
        conn.close()
        if movie:
            formatted_movie = {
                "title": movie[0],
                "original_title": movie[1],
                "release_date": movie[2],
                "budget": movie[3],
                "revenue": movie[4],
                "runtime": movie[5],
                "overview": movie[6],
                "production_companies": movie[7],
                "production_countries": movie[8],
                "rating_avg": movie[9],
                "rating_count": movie[10],
                "country": movie[11],
                "poster_path": movie[12],
                "backdrop_path": movie[13],
                "adult": movie[14]
            }
            return jsonify({"movie": formatted_movie}), 200
        else:
            return jsonify({"error": "Movie not found"}), 404
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        return jsonify({"error": "Failed to fetch movie details"}), 500


@app.route('/api/rate_movie', methods=['POST'])
def rate_movie():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        review = data.get('review', '')
        if not user_id or not movie_id or rating is None:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        if not (0 <= rating <= 10):
            return jsonify({"status": "error", "message": "Rating must be between 0 and 10"}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Ratings (user_id, movie_id, rating, review)
            VALUES (?, ?, ?, ?)
        ''', (user_id, movie_id, rating, review))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Rating added successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#favorites
@app.route('/api/get_favourites', methods=['GET'])
def get_favourites():
    user_id = request.args.get('user_id')  # Get user_id from query parameters
    if not user_id:
        return jsonify({"status": "error", "message": "User ID is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch favourites, movie details, and rating details
        cursor.execute("""
            SELECT 
                f.movie_id,
                m.poster_path,
                r.rating,
                r.review,
                r.rated_at,
                f.added_at
            FROM Favorites f
            JOIN Movies m ON f.movie_id = m.movie_id
            JOIN Ratings r ON f.rating_id = r.rating_id
            WHERE f.user_id = ?
            ORDER BY f.added_at DESC
        """, (user_id,))

        favourites = cursor.fetchall()
        conn.close()

        # Format the results as a list of dictionaries
        result = [
            {
                "movie_id": fav[0],
                "poster_path": fav[1],
                "rating": fav[2],
                "review": fav[3],
                "rated_at": fav[4],
                "added_at": fav[5]
            }
            for fav in favourites
        ]

        return jsonify({"status": "success", "favourites": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/remove_favourite', methods=['DELETE'])
def remove_favourite():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')

        if not user_id or not movie_id:
            return jsonify({"status": "error", "message": "User ID and Movie ID are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete the favourite entry
        cursor.execute("""
            DELETE FROM Favorites 
            WHERE user_id = ? AND movie_id = ?
        """, (user_id, movie_id))

        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Favourite not found"}), 404

        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Favourite removed successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/get_all_users', methods=['GET'])
def getAllUsers():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all users
        query = "SELECT user_id, email, username FROM Users"
        cursor.execute(query)

        # Fetch all results as a list of dictionaries
        users = [
            {"user_id": row[0], "email": row[1], "username": row[2]}
            for row in cursor.fetchall()
        ]

        # Close the connection
        conn.close()

        # Return the response
        return jsonify({"status": "success", "users": users})

    except Exception as e:
        # Handle errors
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/get_all_ratings', methods=['GET'])
def get_all_ratings():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query to get all ratings along with user and movie details
        query = '''
            SELECT r.rating_id, r.rating, r.review, r.user_id, r.movie_id, u.username, m.title AS movie_title
            FROM Ratings r
            JOIN Users u ON r.user_id = u.user_id
            JOIN Movies m ON r.movie_id = m.movie_id'''  
        
        # Execute the query
        cursor.execute(query)
        ratings = cursor.fetchall()

        # Check if ratings are found
        if ratings:
            # Convert ratings to a list of dictionaries
            ratings_list = []
            for row in ratings:
                ratings_list.append({
                    "rating_id": row["rating_id"],
                    "rating": row["rating"],
                    "review": row["review"],
                    "user_id": row["user_id"],
                    "username": row["username"],
                    "movie_id": row["movie_id"],
                    "movie_title": row["movie_title"]
                })
            
            # Close the connection
            conn.close()

            return jsonify({"status": "success", "ratings": ratings_list}), 200
        else:
            return jsonify({"status": "success", "message": "No ratings found"}), 404
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/add_favourite', methods=['POST'])
def add_to_favorites():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")

        user_id = data.get('user_id')
        movie_id = data.get('movie_id')

        if not user_id or not movie_id:
            return jsonify({"message": "user_id and movie_id are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM Favorites WHERE user_id = ? AND movie_id = ?
        ''', (user_id, movie_id))
        exists = cursor.fetchone()[0]

        if exists:
            return jsonify({"success": False, "message": "Movie is already in favorites"}), 409

        # Insert the favorite
        cursor.execute('''
            INSERT INTO Favorites (user_id, movie_id) 
            VALUES (?, ?)
        ''', (user_id, movie_id))
        conn.commit()
        conn.close()

        app.logger.info(f"Movie {movie_id} added to user {user_id}'s favorites.")
        return jsonify({"success": True, "message": "Movie added to favorites"}), 200

    except sqlite3.IntegrityError as e:
        return jsonify({"success": False, "message": "Integrity error: " + str(e)}), 409

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
 

@app.route('/api/remove_favorite', methods=['POST'])
def remove_from_favorites():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')

        if not user_id or not movie_id:
            return jsonify({"message": "user_id and movie_id are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM Favorites WHERE user_id = ? AND movie_id = ?
        ''', (user_id, movie_id))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Movie removed from favorites"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/api/check_favourite', methods=['GET'])
def check_favorite():
    try:
        user_id = request.args.get('user_id')
        movie_id = request.args.get('movie_id')
        if not user_id or not movie_id:
            return jsonify({"message": "user_id and movie_id are required"}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count 
            FROM Favorites 
            WHERE user_id = ? AND movie_id = ?
        ''', (user_id, movie_id))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            is_favourite = False
        else:
            is_favourite = result[0] > 0
        return jsonify({"is_favourite": is_favourite}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/api/get_movie_count', methods=['GET'])
def get_movie_count():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Movies")
        count = cursor.fetchone()[0]
        conn.close()
        return jsonify({"status": "success", "count": count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/')
def home():
    return 'Welcome to the Movies API!'


if __name__ == "__main__":
    app.run(debug=True)

