from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import re
import bcrypt

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

    # Validate the user credentials
    if user and user['password'] == password:
        return jsonify({"success": True, "message": "Login successful"})
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
            "genres": movie[6]
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
    

@app.route("/api/latest", methods=["GET"])
def latest_movies():
    limit = request.args.get("limit", default=10, type=int)
    conn = sqlite3.connect('movies.db')  
    cursor = conn.cursor()
    # Query to fetch the latest movies
    query = """
    SELECT m.poster_path
    FROM Movies m
    ORDER BY m.release_date DESC
    LIMIT ?
    """
    
    try:
        # Execute query with limit
        cursor.execute(query, (limit,))
        movies = cursor.fetchall()
        conn.close()
        formatted_movies = [
            {"poster_path": movie[0]} for movie in movies
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
    SELECT m.poster_path
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
            {"poster_path": movie[0]} for movie in movies
        ]
        return jsonify({"movies": formatted_movies}), 200
    
    except Exception as e:
        print(f"Error fetching top rated movies: {e}")
        return jsonify({"error": "Failed to fetch top rated movies"}), 500
    

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
        SELECT m.poster_path
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
                {"poster_path": movie[0]} for movie in movies
            ]
            return jsonify({"movies": formatted_movies}), 200
        except Exception as e:
            print(f"Error fetching genre movies: {e}")
            return jsonify({"error": "Failed to fetch genre movies"}), 500
    else:
        return jsonify({"error": "Genre not found"}), 404


@app.route("/api/search_movie", methods=["GET"])
def search_movies():
    query = request.args.get("query", type=str)
    limit = request.args.get("limit", default=10, type=int)
    
    # Fetch movies that match the search query
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    query = """
    SELECT m.poster_path
    FROM Movies m
    WHERE m.title LIKE ?
    LIMIT ?
    """
    
    try:
        cursor.execute(query, (f"%{query}%", limit))
        movies = cursor.fetchall()
        conn.close()
        formatted_movies = [
            {"poster_path": movie[0]} for movie in movies
        ]
        return jsonify({"movies": formatted_movies}), 200
    except Exception as e:
        print(f"Error fetching search movies: {e}")
        return jsonify({"error": "Failed to fetch search movies"}), 500
    


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

@app.route('/')
def home():
    return 'Welcome to the Movies API!'

if __name__ == "__main__":
    app.run(debug=True)

