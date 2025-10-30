from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum

class Category(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    OTHER = "other"
    UNCATEGORIZED = "uncategorized"

@dataclass
class Expense:
    id: int = None
    date: str = ""  # ISO format YYYY-MM-DD
    amount: float = 0.0
    currency: str = "USD"
    category: Category = Category.UNCATEGORIZED
    description: str = ""
    method: str = "cash"  # cash or card
    tags: List[str] = field(default_factory=list)

@dataclass
class Budget:
    month: str = ""  # YYYY-MM
    category_limits: Dict[str, float] = field(default_factory=dict)
    savings_goal: float = 0.0

@dataclass
class UserPrefs:
    currency: str = "USD"
    income: float = 0.0
    savings_goal: float = 0.0
