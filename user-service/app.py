from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = 'users.db'

def init_db():
    if not os.path.exists(DB):  # Evita sobreescritura en cada inicio
        with sqlite3.connect(DB) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            print("Base de datos inicializada.")

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    with sqlite3.connect(DB) as conn:
        try:
            conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (data['name'], data['email']))
            conn.commit()
            return {"msg": "User created"}, 201
        except sqlite3.IntegrityError:
            return {"error": "Email must be unique"}, 400

@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect(DB) as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
        return jsonify([dict(zip(['id', 'name', 'email'], user)) for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with sqlite3.connect(DB) as conn:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            return dict(zip(['id', 'name', 'email'], user))
        return {"error": "User not found"}, 404

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    init_db()  # Llamada manual
    app.run(host='0.0.0.0', port=5000)
