from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'dailybasisroute-secret-key-2025'

# Configuração do banco de dados
DATABASE = 'dailybasisroute.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de tarefas (definições)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            emoji TEXT,
            points REAL NOT NULL,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de registros diários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            task_id INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (task_id) REFERENCES tasks (id),
            UNIQUE(user_id, date, task_id)
        )
    ''')
    
    # Tabela de notas diárias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, date)
        )
    ''')
    
    # Tabela de streaks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            current_streak INTEGER DEFAULT 0,
            last_completion_date DATE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de tarefas customizadas do dia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            name TEXT NOT NULL,
            points INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def setup_default_tasks(user_id):
    """Cria as tarefas padrão para um novo usuário"""
    conn = get_db()
    cursor = conn.cursor()
    
    default_tasks = {
        'pilares': [
            {'name': 'Devocional Diário', 'emoji': '🙏', 'points': 20, 'details': 'Manhã OU noite - 25min'},
            {'name': 'Dormiu antes das 23h', 'emoji': '😴', 'points': 10, 'details': 'Rotina de sono'},
            {'name': 'Acordou cedo sem voltar', 'emoji': '⏰', 'points': 10, 'details': 'Acordou e levantou!'},
        ],
        'cardapio': [
            {'name': 'Atividade Física', 'emoji': '💪', 'points': 15, 'details': 'Academia, pedal, corrida - qualquer tipo'},
            {'name': 'Estudo DS/Python', 'emoji': '📊', 'points': 15, 'details': '1-2h focado'},
            {'name': 'Inglês', 'emoji': '🗣️', 'points': 10, 'details': '30min-1h de prática'},
            {'name': 'SQL Prático', 'emoji': '🗄️', 'points': 10, 'details': '30min-1h praticando'},
            {'name': 'Leitura', 'emoji': '📖', 'points': 10, 'details': 'Livros técnicos, artigos'},
        ],
        'bonus': [
            {'name': 'Anotou no Obsidian', 'emoji': '📝', 'points': 5, 'details': 'Documentou aprendizado'},
            {'name': 'Treino Focado <1h30', 'emoji': '⚡', 'points': 5, 'details': 'Academia eficiente'},
            {'name': 'Pedal Extra', 'emoji': '🚴', 'points': 10, 'details': 'Além da atividade física'},
        ]
    }
    
    for category, tasks_list in default_tasks.items():
        for task in tasks_list:
            cursor.execute('''
                INSERT INTO tasks (user_id, category, name, emoji, points, details)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, category, task['name'], task['emoji'], task['points'], task['details']))
    
    # Criar registro de streak
    cursor.execute('INSERT INTO streaks (user_id) VALUES (?)', (user_id,))
    
    conn.commit()
    conn.close()

# Rotas
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('index', error='invalid'))

@app.route('/cadastro', methods=['POST'])
def cadastro():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (email, password_hash, name)
            VALUES (?, ?, ?)
        ''', (email, generate_password_hash(password), name))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Setup tarefas padrão
        setup_default_tasks(user_id)
        
        session['user_id'] = user_id
        session['user_name'] = name
        conn.close()
        return redirect(url_for('dashboard'))
    except sqlite3.IntegrityError:
        conn.close()
        return redirect(url_for('index', error='exists'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    today = datetime.now().date().isoformat()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar tarefas do usuário
    tasks = cursor.execute('''
        SELECT t.*, 
               COALESCE(dl.completed, 0) as completed
        FROM tasks t
        LEFT JOIN daily_logs dl ON t.id = dl.task_id 
            AND dl.user_id = ? AND dl.date = ?
        WHERE t.user_id = ?
        ORDER BY t.category, t.id
    ''', (user_id, today, user_id)).fetchall()
    
    # Buscar tarefas customizadas do dia
    custom_tasks = cursor.execute('''
        SELECT * FROM custom_tasks 
        WHERE user_id = ? AND date = ?
        ORDER BY id
    ''', (user_id, today)).fetchall()
    
    # Buscar nota do dia
    note = cursor.execute('''
        SELECT content FROM notes WHERE user_id = ? AND date = ?
    ''', (user_id, today)).fetchone()
    
    # Buscar streak
    streak_data = cursor.execute('''
        SELECT current_streak FROM streaks WHERE user_id = ?
    ''', (user_id,)).fetchone()
    
    conn.close()
    
    # Organizar tarefas por categoria
    tasks_by_category = {'pilares': [], 'cardapio': [], 'bonus': []}
    for task in tasks:
        tasks_by_category[task['category']].append(dict(task))
    
    return render_template('dashboard.html',
                         tasks=tasks_by_category,
                         custom_tasks=[dict(ct) for ct in custom_tasks],
                         note=note['content'] if note else '',
                         streak=streak_data['current_streak'] if streak_data else 0,
                         today=today)

@app.route('/api/toggle_task', methods=['POST'])
def toggle_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    task_id = request.json.get('task_id')
    date = request.json.get('date', datetime.now().date().isoformat())
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar se já existe um registro
    existing = cursor.execute('''
        SELECT completed FROM daily_logs 
        WHERE user_id = ? AND task_id = ? AND date = ?
    ''', (user_id, task_id, date)).fetchone()
    
    if existing:
        # Toggle
        new_status = 0 if existing['completed'] else 1
        cursor.execute('''
            UPDATE daily_logs SET completed = ? 
            WHERE user_id = ? AND task_id = ? AND date = ?
        ''', (new_status, user_id, task_id, date))
    else:
        # Criar novo
        cursor.execute('''
            INSERT INTO daily_logs (user_id, task_id, date, completed)
            VALUES (?, ?, ?, 1)
        ''', (user_id, task_id, date))
    
    conn.commit()
    
    # Calcular pontos totais do dia (tarefas normais + customizadas)
    points = cursor.execute('''
        SELECT SUM(t.points) as total
        FROM daily_logs dl
        JOIN tasks t ON dl.task_id = t.id
        WHERE dl.user_id = ? AND dl.date = ? AND dl.completed = 1
    ''', (user_id, date)).fetchone()
    
    custom_points = cursor.execute('''
        SELECT SUM(points) as total
        FROM custom_tasks
        WHERE user_id = ? AND date = ?
    ''', (user_id, date)).fetchone()
    
    total_points = (points['total'] if points['total'] else 0) + (custom_points['total'] if custom_points['total'] else 0)
    
    # Atualizar streak se necessário
    update_streak(user_id, date, total_points)
    
    conn.close()
    
    return jsonify({'success': True, 'total_points': total_points})

@app.route('/api/save_note', methods=['POST'])
def save_note():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    content = request.json.get('content')
    date = request.json.get('date', datetime.now().date().isoformat())
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO notes (user_id, date, content)
        VALUES (?, ?, ?)
    ''', (user_id, date, content))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/add_custom_task', methods=['POST'])
def add_custom_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    name = request.json.get('name')
    points = request.json.get('points')
    date = request.json.get('date', datetime.now().date().isoformat())
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO custom_tasks (user_id, date, name, points, completed)
        VALUES (?, ?, ?, ?, 1)
    ''', (user_id, date, name, points))
    
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'task_id': task_id})

@app.route('/api/delete_custom_task', methods=['POST'])
def delete_custom_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    task_id = request.json.get('task_id')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM custom_tasks 
        WHERE id = ? AND user_id = ?
    ''', (task_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/stats')
def get_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Últimos 7 dias
    week_data = cursor.execute('''
        SELECT dl.date, SUM(t.points) as points
        FROM daily_logs dl
        JOIN tasks t ON dl.task_id = t.id
        WHERE dl.user_id = ? AND dl.completed = 1
            AND dl.date >= date('now', '-7 days')
        GROUP BY dl.date
        ORDER BY dl.date
    ''', (user_id,)).fetchall()
    
    # Últimos 30 dias
    month_data = cursor.execute('''
        SELECT dl.date, SUM(t.points) as points
        FROM daily_logs dl
        JOIN tasks t ON dl.task_id = t.id
        WHERE dl.user_id = ? AND dl.completed = 1
            AND dl.date >= date('now', '-30 days')
        GROUP BY dl.date
        ORDER BY dl.date
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'week': [{'date': row['date'], 'points': row['points']} for row in week_data],
        'month': [{'date': row['date'], 'points': row['points']} for row in month_data]
    })

@app.route('/api/export')
def export_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Buscar todos os dados
    logs = cursor.execute('''
        SELECT dl.date, t.name, t.category, t.points, dl.completed, n.content as note
        FROM daily_logs dl
        JOIN tasks t ON dl.task_id = t.id
        LEFT JOIN notes n ON dl.user_id = n.user_id AND dl.date = n.date
        WHERE dl.user_id = ?
        ORDER BY dl.date DESC
    ''', (user_id,)).fetchall()
    
    # Buscar tarefas customizadas
    custom_logs = cursor.execute('''
        SELECT date, name, points
        FROM custom_tasks
        WHERE user_id = ?
        ORDER BY date DESC
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    # Organizar dados por dia
    data_by_date = {}
    for log in logs:
        date = log['date']
        if date not in data_by_date:
            data_by_date[date] = {
                'date': date,
                'tasks': [],
                'total_points': 0,
                'note': log['note']
            }
        
        if log['completed']:
            data_by_date[date]['tasks'].append({
                'name': log['name'],
                'category': log['category'],
                'points': log['points']
            })
            data_by_date[date]['total_points'] += log['points']
    
    # Adicionar tarefas customizadas
    for custom in custom_logs:
        date = custom['date']
        if date not in data_by_date:
            data_by_date[date] = {
                'date': date,
                'tasks': [],
                'total_points': 0,
                'note': None
            }
        
        data_by_date[date]['tasks'].append({
            'name': custom['name'],
            'category': 'custom',
            'points': custom['points']
        })
        data_by_date[date]['total_points'] += custom['points']
    
    return jsonify(list(data_by_date.values()))

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('analytics.html')

@app.route('/historico')
def historico():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Últimos 30 dias com pontos
    history = cursor.execute('''
        SELECT 
            dl.date,
            SUM(t.points) as total_points,
            COUNT(DISTINCT CASE WHEN dl.completed = 1 THEN t.id END) as completed_tasks,
            n.content as note
        FROM daily_logs dl
        JOIN tasks t ON dl.task_id = t.id
        LEFT JOIN notes n ON dl.user_id = n.user_id AND dl.date = n.date
        WHERE dl.user_id = ? AND dl.date >= date('now', '-30 days')
        GROUP BY dl.date
        ORDER BY dl.date DESC
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return render_template('historico.html', history=[dict(row) for row in history])

def update_streak(user_id, current_date, points):
    """Atualiza a sequência do usuário"""
    conn = get_db()
    cursor = conn.cursor()
    
    streak = cursor.execute('SELECT * FROM streaks WHERE user_id = ?', (user_id,)).fetchone()
    
    if not streak:
        cursor.execute('INSERT INTO streaks (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()
        return
    
    current_streak = streak['current_streak']
    last_date = streak['last_completion_date']
    
    # Se bateu 60+ pontos
    if points >= 60:
        if last_date:
            last_date_obj = datetime.fromisoformat(last_date).date()
            current_date_obj = datetime.fromisoformat(current_date).date()
            diff = (current_date_obj - last_date_obj).days
            
            if diff == 1:
                # Dia consecutivo
                current_streak += 1
            elif diff == 0:
                # Mesmo dia, não faz nada
                pass
            else:
                # Quebrou a sequência
                current_streak = 1
        else:
            current_streak = 1
        
        cursor.execute('''
            UPDATE streaks 
            SET current_streak = ?, last_completion_date = ?
            WHERE user_id = ?
        ''', (current_streak, current_date, user_id))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
