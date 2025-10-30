import sqlite3
from typing import List, Dict, Any
from models import Expense, Budget, UserPrefs, Category

class Database:
    def __init__(self, db_path: str = "finance.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    method TEXT NOT NULL,
                    tags TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month TEXT NOT NULL UNIQUE,
                    category_limits TEXT NOT NULL,
                    savings_goal REAL NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_prefs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    currency TEXT NOT NULL,
                    income REAL NOT NULL,
                    savings_goal REAL NOT NULL
                )
            ''')
            conn.commit()

    def insert_expense(self, expense: Expense) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (date, amount, currency, category, description, method, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (expense.date, expense.amount, expense.currency, expense.category.value,
                  expense.description, expense.method, ','.join(expense.tags)))
            conn.commit()
            return cursor.lastrowid

    def get_expenses(self, month: str = None) -> List[Expense]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if month:
                cursor.execute('SELECT * FROM expenses WHERE strftime("%Y-%m", date) = ?', (month,))
            else:
                cursor.execute('SELECT * FROM expenses')
            rows = cursor.fetchall()
            expenses = []
            for row in rows:
                expense = Expense(
                    id=row[0],
                    date=row[1],
                    amount=row[2],
                    currency=row[3],
                    category=Category(row[4]),
                    description=row[5],
                    method=row[6],
                    tags=row[7].split(',') if row[7] else []
                )
                expenses.append(expense)
            return expenses

    def update_budget(self, budget: Budget):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO budgets (month, category_limits, savings_goal)
                VALUES (?, ?, ?)
            ''', (budget.month, str(budget.category_limits), budget.savings_goal))
            conn.commit()

    def get_budget(self, month: str) -> Budget:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM budgets WHERE month = ?', (month,))
            row = cursor.fetchone()
            if row:
                return Budget(
                    month=row[1],
                    category_limits=eval(row[2]),  # Safe since we control the data
                    savings_goal=row[3]
                )
            return Budget()

    def update_user_prefs(self, prefs: UserPrefs):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_prefs (id, currency, income, savings_goal)
                VALUES (1, ?, ?, ?)
            ''', (prefs.currency, prefs.income, prefs.savings_goal))
            conn.commit()

    def get_user_prefs(self) -> UserPrefs:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_prefs WHERE id = 1')
            row = cursor.fetchone()
            if row:
                return UserPrefs(
                    currency=row[1],
                    income=row[2],
                    savings_goal=row[3]
                )
            return UserPrefs()
