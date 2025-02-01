from flask import Flask, jsonify
import sqlite3

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
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) NOT NULL UNIQUE CHECK(email LIKE '%_@__%.__%'),
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL DEFAULT 'user' CHECK(role IN ('user', 'admin'))
    );
''')

#Ratings Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ratings (
                rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                rating INT NOT NULL CHECK(rating >= 0 AND rating <= 10),
                review TEXT,
                rated_at DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);
''')
#Favorites Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS Favorites (
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                added_at DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                UNIQUE (user_id, movie_id)
            )
''')
#WatchLater table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS WatchLater (
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                added_at DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
                UNIQUE (user_id, movie_id)
            )
''')


#MovieLogs Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS MovieLogs (
            movie_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            movie_id INTEGER,       
            action TEXT NOT NULL CHECK(action IN ('Add', 'Delete', 'Update')),    
            details TEXT,              
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES Users(user_id)
            )
''')

#UserLogs Table
cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserLogs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL, 
            user_id INTEGER,
            action TEXT NOT NULL CHECK(action IN ('Add', 'Delete', 'Update')),
            old_data TEXT,  
            new_data TEXT,  
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES Users(user_id)
            )
''')
# Commit the changes and close the connection
conn.commit()
conn.close()


@app.route('/')
def home():
    return 'Welcome to the Movies API!'

if __name__ == '__main__':
    app.run(debug=True)