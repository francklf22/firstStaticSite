from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os

app = Flask(__name__)

DB_FILE = 'auth.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    print('\n=== LOGIN REQUEST RECEIVED ===')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(f'Username: {username}')
    print(f'Password: {password}')

    if not username or not password:
        print('ERROR: Username or password missing')
        return jsonify({'success': False, 'message': 'Username and password required'}), 400

    print(f'Connecting to database: {DB_FILE}')
    conn = get_db_connection()
    cursor = conn.cursor()
    print(f'Querying user: {username}')
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print(f'User found in database')
        stored_hash = result[0]
        print(f'Stored hash: {stored_hash[:20]}... (truncated)')
        print(f'Checking password...')
        password_match = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        print(f'Password match: {password_match}')
        if password_match:
            print('LOGIN SUCCESSFUL')
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            print('LOGIN FAILED: Password mismatch')
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    else:
        print(f'LOGIN FAILED: User not found')
        return jsonify({'success': False, 'message': 'Invalid credentials'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)