# Database.py
import sqlite3
from datetime import datetime, timedelta

DB_NAME = "dashboard.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # USERS
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    role TEXT,
                    department TEXT,
                    sub_department TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    # DEVICES
    c.execute('''CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT,
                    device_type TEXT,
                    model TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    # DEPARTMENTS
    c.execute('''CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    parent_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES departments (id)
                )''')

    conn.commit()
    conn.close()

# ---------- USERS ----------
def add_user(first_name, last_name, email, role, department, sub_department):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""INSERT INTO users (first_name, last_name, email, role, department, sub_department)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (first_name, last_name, email, role, department, sub_department))
    conn.commit()
    conn.close()

def get_recent_users(limit=5):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT first_name, last_name, email, department, sub_department, created_at 
                 FROM users ORDER BY created_at DESC LIMIT ?""", (limit,))
    data = c.fetchall()
    conn.close()
    return data

def get_users_by_department(dept_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT first_name, last_name, email, sub_department FROM users WHERE department=?", (dept_name,))
    data = c.fetchall()
    conn.close()
    return data

def get_users_by_sub_department(sub_dept_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT first_name, last_name, email FROM users WHERE sub_department=?", (sub_dept_name,))
    data = c.fetchall()
    conn.close()
    return data

def get_user_growth():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    six_months_ago = datetime.now() - timedelta(days=180)
    c.execute("SELECT DATE(created_at), COUNT(*) FROM users WHERE created_at >= ? GROUP BY DATE(created_at)", (six_months_ago,))
    data = c.fetchall()
    conn.close()
    return data

# ---------- DEVICES ----------
def add_device(serial_number, device_type, model):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO devices (serial_number, device_type, model) VALUES (?, ?, ?)",
              (serial_number, device_type, model))
    conn.commit()
    conn.close()

def get_all_devices():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, serial_number, device_type, model, created_at FROM devices ORDER BY created_at DESC")
    data = c.fetchall()
    conn.close()
    return data

def update_device(device_id, serial_number, device_type, model):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE devices SET serial_number=?, device_type=?, model=? WHERE id=?",
              (serial_number, device_type, model, device_id))
    conn.commit()
    conn.close()

def delete_device(device_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE id=?", (device_id,))
    conn.commit()
    conn.close()

# ---------- DEPARTMENTS ----------
def add_department(name, parent_id=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO departments (name, parent_id) VALUES (?, ?)", (name, parent_id))
    conn.commit()
    conn.close()

def get_departments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, parent_id FROM departments ORDER BY name ASC")
    data = c.fetchall()
    conn.close()
    return data

def get_parent_departments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name FROM departments WHERE parent_id IS NULL ORDER BY name ASC")
    data = c.fetchall()
    conn.close()
    return data

def get_sub_departments(parent_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name FROM departments WHERE parent_id=? ORDER BY name ASC", (parent_id,))
    data = c.fetchall()
    conn.close()
    return data

def update_department(dept_id, new_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE departments SET name=? WHERE id=?", (new_name, dept_id))
    conn.commit()
    conn.close()
