import mysql.connector
import bcrypt

# Connect to MySQL (without database)
conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Change if needed
    password=''   # Set your MySQL root password
)
cursor = conn.cursor()

# Create database
cursor.execute('CREATE DATABASE IF NOT EXISTS auth_db')
conn.commit()

# Connect to the database
conn.database = 'auth_db'

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
''')
conn.commit()

# Insert a sample user (username: admin, password: password)
hashed = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
cursor.execute('INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)', ('admin', hashed.decode('utf-8')))
conn.commit()

conn.close()
print('Database setup complete. Sample user: admin / password')