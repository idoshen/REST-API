from flask import Flask, request, jsonify, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('user_management.db')
    except Error as e:
        print(e)
    return conn

def execute_query(query, args=()):
    """ Execute a single query """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()

def execute_read_query(query, args=()):
    """ Execute a single read query """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    conn.close()
    return result

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    print(name, email, password)
    execute_query('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    return jsonify({'name': name, 'email': email}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = execute_read_query('SELECT * FROM users')
    return jsonify(users)

@app.route('/users/<identifier>', methods=['GET'])
def get_user(identifier):
    if "@" in identifier:  # Check if the identifier is an email
        query = 'SELECT * FROM users WHERE email = ?'
        params = (identifier,)
    elif identifier.isdigit():  # Check if the identifier is all digits (ID)
        user_id = int(identifier)
        query = 'SELECT * FROM users WHERE id = ?'
        params = (user_id,)
    else:  # Assume the identifier is a name
        query = 'SELECT * FROM users WHERE name = ?'
        params = (identifier,)
    
    user = execute_read_query(query, params)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user[0])

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    execute_query('UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?', (name, email, password, id))
    return jsonify({'id': id, 'name': name, 'email': email})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    if not execute_read_query('SELECT * FROM users WHERE id = ?', (id,)):
        return jsonify({'message': 'User not found'}), 404
    execute_query('DELETE FROM users WHERE id = ?', (id,))
    return jsonify({'message': 'User deleted successfully.'})

@app.route('/')
def loadWebPage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
