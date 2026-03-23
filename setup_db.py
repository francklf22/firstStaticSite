import sqlite3
import bcrypt

DB_FILE = 'auth.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
conn.commit()

# Insert a sample user (username: admin, password: password)
hashed = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
cursor.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)', ('admin', hashed.decode('utf-8')))
conn.commit()

conn.close()
print('Database setup complete. Sample user: admin / password')