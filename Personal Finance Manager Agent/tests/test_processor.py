import pytest
from models import Expense, Budget, Category
from processor import Processor
from datetime import datetime

def test_categorize_expense():
    assert Processor.categorize_expense("Lunch at restaurant") == Category.FOOD
    assert Processor.categorize_expense("Bus fare") == Category.TRANSPORT
    assert Processor.categorize_expense("Movie tickets") == Category.ENTERTAINMENT
    assert Processor.categorize_expense("Electricity bill") == Category.UTILITIES
    assert Processor.categorize_expense("Doctor visit") == Category.HEALTHCARE
    assert Processor.categorize_expense("Random expense") == Category.UNCATEGORIZED

def test_aggregate_expenses():
    expenses = [
        Expense(date="2023-10-01", amount=100, category=Category.FOOD),
        Expense(date="2023-10-02", amount=50, category=Category.TRANSPORT),
        Expense(date="2023-10-01", amount=75, category=Category.FOOD)
    ]
    result = Processor.aggregate_expenses(expenses, "2023-10")
    assert result['total'] == 225
    assert result['by_category']['food'] == 175
    assert result['by_category']['transport'] == 50

def test_calculate_budget_status():
    expenses = [
        Expense(date="2023-10-01", amount=100, category=Category.FOOD),
        Expense(date="2023-10-02", amount=50, category=Category.TRANSPORT)
    ]
    budget = Budget(month="2023-10", category_limits={"food": 150, "transport": 100}, savings_goal=200)
    result = Processor.calculate_budget_status(expenses, budget)

    assert result['total_spent'] == 150
    assert result['category_status']['food']['spent'] == 100
    assert result['category_status']['food']['remaining'] == 50
    assert not result['category_status']['food']['over_budget']

def test_generate_saving_tips():
    aggregates = {
        'total': 500,
        'by_category': {'food': 200, 'transport': 100},
        'top_categories': [('food', 200)]
    }
    budget_status = {
        'category_status': {'food': {'spent': 200, 'limit': 150, 'over_budget': True}},
        'budget_gap': -50
    }
    tips = Processor.generate_saving_tips(aggregates, budget_status)
    assert len(tips) <= 3
    assert 'tip' in tips[0]
    assert 'estimated_savings' in tips[0]
    assert 'confidence' in tips[0]
    assert 'math' in tips[0]
