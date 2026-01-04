-- Script para inicializar o banco de dados DailyBasisRoute no Supabase
-- Execute este script no SQL Editor do Supabase

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de tarefas (definições)
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    emoji TEXT,
    points REAL NOT NULL,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Tabela de registros diários
CREATE TABLE IF NOT EXISTS daily_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    task_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
    UNIQUE(user_id, date, task_id)
);

-- Tabela de notas diárias
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    content TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE(user_id, date)
);

-- Tabela de streaks
CREATE TABLE IF NOT EXISTS streaks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    current_streak INTEGER DEFAULT 0,
    last_completion_date DATE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Tabela de tarefas customizadas do dia
CREATE TABLE IF NOT EXISTS custom_tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    name TEXT NOT NULL,
    points INTEGER NOT NULL,
    completed BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Tabela de humor diário
CREATE TABLE IF NOT EXISTS daily_mood (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    mood_score INTEGER NOT NULL CHECK (mood_score >= 0 AND mood_score <= 100),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE(user_id, date)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_daily_logs_user_date ON daily_logs(user_id, date);
CREATE INDEX IF NOT EXISTS idx_notes_user_date ON notes(user_id, date);
CREATE INDEX IF NOT EXISTS idx_custom_tasks_user_date ON custom_tasks(user_id, date);
CREATE INDEX IF NOT EXISTS idx_tasks_user ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_mood_user_date ON daily_mood(user_id, date);

-- Mensagem de sucesso
SELECT 'Tabelas criadas com sucesso!' as message;
