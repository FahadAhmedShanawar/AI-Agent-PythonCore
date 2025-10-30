from typing import List
from models import Expense, Budget, UserPrefs
from db import Database

class Storage:
    def __init__(self, db: Database):
        self.db = db

    def save_expense(self, expense: Expense) -> int:
        return self.db.insert_expense(expense)

    def load_expenses(self, month: str = None) -> List[Expense]:
        return self.db.get_expenses(month)

    def save_budget(self, budget: Budget):
        self.db.update_budget(budget)

    def load_budget(self, month: str) -> Budget:
        return self.db.get_budget(month)

    def save_user_prefs(self, prefs: UserPrefs):
        self.db.update_user_prefs(prefs)

    def load_user_prefs(self) -> UserPrefs:
        return self.db.get_user_prefs()
