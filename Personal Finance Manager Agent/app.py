from flask import Flask, request, jsonify, render_template
import os
from db import Database
from storage import Storage
from processor import Processor
from openai_client import OpenAIClient
from ui_helpers import UIHelpers
from models import Expense, Budget, UserPrefs, Category
from utils import parse_date, format_currency
import json

app = Flask(__name__)
db = Database()
storage = Storage(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expense', methods=['POST'])
def add_expense():
    data = request.json
    try:
        expense = Expense(
            date=parse_date(data['date']),
            amount=float(data['amount']),
            currency=data.get('currency', 'USD'),
            category=Processor.categorize_expense(data['description']),
            description=data['description'],
            method=data.get('method', 'cash'),
            tags=data.get('tags', [])
        )
        expense_id = storage.save_expense(expense)
        return jsonify({'id': expense_id, 'message': 'Expense added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    month = request.args.get('month')
    expenses = storage.load_expenses(month)
    budget = storage.load_budget(month or 'current')

    aggregates = Processor.aggregate_expenses(expenses, month)
    budget_status = Processor.calculate_budget_status(expenses, budget)

    # Generate tips
    try:
        client = OpenAIClient()
        tips = client.generate_tips(aggregates, budget_status)
    except:
        tips = Processor.generate_saving_tips(aggregates, budget_status)

    charts = {
        'pie_chart': UIHelpers.create_pie_chart(aggregates['by_category']),
        'bar_chart': UIHelpers.create_bar_chart(aggregates['by_category'])
    }

    return jsonify({
        'aggregates': aggregates,
        'budget_status': budget_status,
        'charts': charts,
        'tips': tips
    })

@app.route('/api/budget', methods=['POST'])
def set_budget():
    data = request.json
    try:
        budget = Budget(
            month=data['month'],
            category_limits=data['category_limits'],
            savings_goal=float(data['savings_goal'])
        )
        storage.save_budget(budget)
        return jsonify({'message': 'Budget updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/tips', methods=['POST'])
def get_tips():
    month = request.json.get('month')
    expenses = storage.load_expenses(month)
    budget = storage.load_budget(month or 'current')

    aggregates = Processor.aggregate_expenses(expenses, month)
    budget_status = Processor.calculate_budget_status(expenses, budget)

    # Try OpenAI first, fallback to rule-based
    try:
        client = OpenAIClient()
        tips = client.generate_tips(aggregates, budget_status)
    except:
        tips = Processor.generate_saving_tips(aggregates, budget_status)

    return jsonify({'tips': tips})

@app.route('/api/user_prefs', methods=['POST'])
def set_user_prefs():
    data = request.json
    try:
        prefs = UserPrefs(
            currency=data.get('currency', 'USD'),
            income=float(data.get('income', 0)),
            savings_goal=float(data.get('savings_goal', 0))
        )
        storage.save_user_prefs(prefs)
        return jsonify({'message': 'Preferences updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
