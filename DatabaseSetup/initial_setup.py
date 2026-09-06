import sqlite3
import os

DB_PATH = 'Database/game_recommendation_system.db'

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                genre_id INTEGER,
                FOREIGN KEY (game_id) REFERENCES video_games(id) ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_toxicity_prevalence_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                insults_flaming REAL DEFAULT 0.0,
                hate_harassment REAL DEFAULT 0.0,
                offensive_texts REAL DEFAULT 0.0,
                FOREIGN KEY (game_id) REFERENCES video_games(id) ON DELETE CASCADE
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                genre_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
            )
        ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_toxicity_tolerance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                insults_flaming REAL DEFAULT 1.0,
                hate_harassment REAL DEFAULT 1.0,
                offensive_texts REAL DEFAULT 1.0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')