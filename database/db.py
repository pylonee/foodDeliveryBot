# база данных

import sqlite3
import json
from datetime import datetime
from typing import Optional
from database.models import User, Order, MenuItem
from config import DB_CONFIG


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(**DB_CONFIG)
        self._create_tables()

    def _create_tables(self):
        # Создаём таблицы
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            address TEXT,
            registration_date TEXT
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            items TEXT,
            total REAL,
            address TEXT,
            status TEXT,
            order_date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            price REAL,
            category TEXT,
            available TEXT
        )''')

        self.conn.commit()

    def close(self):
        # Закрываем соединение с БД
        self.conn.close()


    # =======================================  Client functions  =======================================
    def add_client(self, user: User) -> bool:
        # Добавляем нового пользователя
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO users 
                (user_id, username, first_name, last_name, phone, address, registration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (user.user_id, user.username, user.first_name,
                 user.last_name, user.phone, user.address,
                 user.registration_date.isoformat())
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False

    def get_client_by_id(self, user_id: int) -> Optional[User]:
        # Получаем пользователя по ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if row:
            return User(
                user_id=row[0],
                username=row[1],
                first_name=row[2],
                last_name=row[3],
                phone=row[4],
                address=row[5],
                registration_date=datetime.fromisoformat(row[6]))
        return None

    def remove_client_by_id(self, user_id: int) -> bool:
        # Удаляем пользователя по ID
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?;", (user_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")
            return False

    # =======================================  Product menu functions  =======================================
    def add_menu_item(self, item: MenuItem) -> Optional[int]:
        #Добавляем новую позицию в меню
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO menu
                (item_id, name, description, price, category, available)
                VALUES(?, ?, ?, ?, ?, ?)''',
                (item.item_id, item.name, item.description, item.price, item.category, item.available,)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении меню: {e}")
            return None

    def get_menu_items(self) -> Optional[list]:
        # Получаем меню
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu")
        rows = cursor.fetchall()

        if rows: return rows

        return None

    def get_menu_item_by_id(self, item_id: int) -> Optional[MenuItem]:
        # Получаем позицию меню по ID
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu WHERE item_id = ?", (item_id,))
        row = cursor.fetchone()

        if row:
            return MenuItem(
                item_id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                category=row[4],
                available=row[5]
            )
        return None

    def remove_menu_item_by_id(self, item_id: int) -> bool:
        # Удаляем позицию меню по ID
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM menu WHERE item_id = ?;", (item_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении позиции: {e}")
            return False

    def remove_menu_items(self) -> bool:
        # Удаляем всё из таблицы меню
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM menu")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка при удалении меню: {e}")
            return False

    # =======================================  Order functions  =======================================
    def add_order(self, order: Order) -> Optional[int]:
        # Добавляем новый заказ
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO orders 
                (user_id, items, total, address, status, order_date)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (order.user_id, json.dumps(order.items, ensure_ascii=False), order.total,
                 order.address, order.status, order.order_date.isoformat())
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении заказа: {e}")
            return None

    def get_orders(self) -> Optional[list]:
        # Получаем список всех заказов
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()

        if rows: return rows

        return None

    def get_order_by_client_id(self, client_id: int) -> Optional[Order]:
        # Получаем активный заказ по ID пользователя
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ? AND status = ?", (client_id, "Active",))
        row = cursor.fetchone()

        if row:
            return Order(
                order_id=row[0],
                user_id=row[1],
                items=json.loads(row[2]),
                total=row[3],
                address=row[4],
                status=row[5],
                order_date=row[6]
            )
        return None