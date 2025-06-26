import requests
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = 'tasks.db'
USER_SERVICE_URL = 'http://user-service:5000/users'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT CHECK(status IN ('pendiente', 'en progreso', 'completada')) NOT NULL DEFAULT 'pendiente',
                user_id INTEGER NOT NULL
            )
        ''')

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    user = requests.get(f'{USER_SERVICE_URL}/{data["user_id"]}')
    if user.status_code != 200:
        return {"error": "Invalid user"}, 400
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO tasks (title, status, user_id) VALUES (?, ?, ?)",
                     (data['title'], data.get('status', 'pendiente'), data['user_id']))
        conn.commit()
        return {"msg": "Task created"}, 201

@app.route('/tasks', methods=['GET'])
def list_tasks():
    user_id = request.args.get('user_id')
    with sqlite3.connect(DB) as conn:
        if user_id:
            tasks = conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        else:
            tasks = conn.execute("SELECT * FROM tasks")
        return jsonify([dict(zip(['id', 'title', 'status', 'user_id'], row)) for row in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT'])
def handle_task(task_id):
    if request.method == 'GET':
        with sqlite3.connect(DB) as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if row:
                return dict(zip(['id', 'title', 'status', 'user_id'], row))
            return {"error": "Not found"}, 404
    else:
        data = request.get_json()
        with sqlite3.connect(DB) as conn:
            conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (data['status'], task_id))
            conn.commit()
            return {"msg": "Task updated"}

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    init_db()  # ✅ Llamada directa para inicializar DB al arrancar el servicio
    app.run(host='0.0.0.0', port=5000)
