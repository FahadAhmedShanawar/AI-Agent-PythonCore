from typing import List, Dict, Tuple
import pandas as pd
from models import Expense, Budget, Category
from utils import extract_keywords

class Processor:
    @staticmethod
    def categorize_expense(description: str) -> Category:
        """Rule-based categorization based on keywords"""
        keywords = extract_keywords(description)
        rules = {
            Category.FOOD: ['food', 'restaurant', 'grocery', 'meal', 'eat', 'drink', 'coffee', 'lunch', 'dinner'],
            Category.TRANSPORT: ['taxi', 'bus', 'train', 'gas', 'fuel', 'uber', 'lyft', 'parking', 'travel'],
            Category.ENTERTAINMENT: ['movie', 'game', 'music', 'concert', 'party', 'fun', 'hobby'],
            Category.UTILITIES: ['electric', 'water', 'gas', 'internet', 'phone', 'utility', 'bill'],
            Category.HEALTHCARE: ['doctor', 'medicine', 'pharmacy', 'health', 'hospital', 'clinic'],
            Category.SHOPPING: ['shop', 'buy', 'purchase', 'store', 'mall', 'clothes', 'amazon']
        }
        for category, cats in rules.items():
            if any(kw in keywords for kw in cats):
                return category
        return Category.UNCATEGORIZED

    @staticmethod
    def aggregate_expenses(expenses: List[Expense], month: str) -> Dict:
        """Aggregate expenses by category and calculate totals"""
        df = pd.DataFrame([{
            'date': e.date,
            'amount': e.amount,
            'category': e.category.value,
            'description': e.description
        } for e in expenses])

        if df.empty:
            return {
                'total': 0.0,
                'by_category': {},
                'top_categories': [],
                'monthly_trend': []
            }

        # Filter by month if specified
        if month:
            df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
            df = df[df['month'] == month]

        total = df['amount'].sum()
        by_category = df.groupby('category')['amount'].sum().to_dict()
        top_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:3]

        # Simple trend (last 7 days vs previous 7)
        df['date'] = pd.to_datetime(df['date'])
        recent = df[df['date'] >= df['date'].max() - pd.Timedelta(days=7)]['amount'].sum()
        previous = df[(df['date'] >= df['date'].max() - pd.Timedelta(days=14)) &
                      (df['date'] < df['date'].max() - pd.Timedelta(days=7))]['amount'].sum()

        trend = (recent - previous) / previous if previous > 0 else 0

        return {
            'total': total,
            'by_category': by_category,
            'top_categories': top_categories,
            'trend': trend
        }

    @staticmethod
    def calculate_budget_status(expenses: List[Expense], budget: Budget) -> Dict:
        """Calculate budget usage and suggestions"""
        aggregates = Processor.aggregate_expenses(expenses, budget.month)
        status = {}

        for cat, limit in budget.category_limits.items():
            spent = aggregates['by_category'].get(cat, 0)
            pct_used = (spent / limit) * 100 if limit > 0 else 0
            remaining = limit - spent
            status[cat] = {
                'spent': spent,
                'limit': limit,
                'pct_used': pct_used,
                'remaining': remaining,
                'over_budget': spent > limit
            }

        total_spent = aggregates['total']
        total_limit = sum(budget.category_limits.values())
        budget_gap = total_limit - total_spent if total_limit > 0 else 0

        return {
            'category_status': status,
            'total_spent': total_spent,
            'total_limit': total_limit,
            'budget_gap': budget_gap,
            'savings_goal': budget.savings_goal
        }

    @staticmethod
    def generate_saving_tips(aggregates: Dict, budget_status: Dict) -> List[Dict]:
        """Generate rule-based saving tips"""
        tips = []
        top_cats = aggregates['top_categories']

        # Tip 1: Reduce spending in top category
        if top_cats:
            cat, amount = top_cats[0]
            reduction = amount * 0.1  # 10% reduction
            tips.append({
                'tip': f"Reduce spending in {cat} by 10%",
                'estimated_savings': reduction,
                'confidence': 'high',
                'math': f"10% of {amount:.2f} = {reduction:.2f}"
            })

        # Tip 2: Address over-budget categories
        over_budget = [cat for cat, stat in budget_status['category_status'].items() if stat['over_budget']]
        if over_budget:
            cat = over_budget[0]
            over_amount = budget_status['category_status'][cat]['spent'] - budget_status['category_status'][cat]['limit']
            tips.append({
                'tip': f"Cut back on {cat} spending",
                'estimated_savings': over_amount,
                'confidence': 'high',
                'math': f"Over budget by {over_amount:.2f}"
            })

        # Tip 3: General tip
        if budget_status['budget_gap'] < 0:
            needed = abs(budget_status['budget_gap'])
            tips.append({
                'tip': "Review and adjust category limits",
                'estimated_savings': needed * 0.5,
                'confidence': 'medium',
                'math': f"Half of budget gap {needed:.2f}"
            })

        return tips[:3]  # Limit to 3 tips
