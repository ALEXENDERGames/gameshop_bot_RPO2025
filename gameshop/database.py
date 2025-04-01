# database.py
import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('orders.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Таблица пользователей
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        reg_date TIMESTAMP)''')

        # Таблица заказов
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        service_name TEXT NOT NULL,
                        description TEXT,
                        status TEXT DEFAULT 'new',
                        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES users(user_id))''')

        self.conn.commit()

    def add_user(self, user_id, username, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO users 
                        (user_id, username, first_name, last_name, reg_date)
                        VALUES (?, ?, ?, ?, ?)''',
                       (user_id, username, first_name, last_name, datetime.now()))
        self.conn.commit()

    def add_order(self, user_id, service_name, description):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO orders 
                        (user_id, service_name, description)
                        VALUES (?, ?, ?)''',
                       (user_id, service_name, description))
        self.conn.commit()
        return cursor.lastrowid

    def get_orders(self, status='new'):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT o.*, u.username 
                        FROM orders o
                        LEFT JOIN users u ON o.user_id = u.user_id
                        WHERE o.status = ?''', (status,))
        return cursor.fetchall()