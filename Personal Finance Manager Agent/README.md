# Personal Finance Manager Agent

A lightweight, privacy-first personal finance management application built with Python and Flask.

## Features

- **Expense Tracking**: Log daily expenses with categorization
- **Budget Management**: Set monthly budgets and track spending against limits
- **Data Visualization**: Interactive charts showing spending patterns
- **AI-Powered Tips**: Generate personalized saving suggestions using OpenAI
- **Privacy-Focused**: All data stored locally, no external uploads

## Tech Stack

- **Backend**: Python 3.10+, Flask
- **Database**: SQLite (built-in)
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **AI**: OpenAI API (optional)
- **Frontend**: HTML/CSS/JavaScript

## Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (optional for AI features):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Usage

### Running the Application

```bash
python app.py
```

Open your browser to `http://localhost:5000`

### Adding Expenses

Use the web interface to add expenses with date, amount, description, and payment method. Expenses are automatically categorized.

### Setting Budgets

Define monthly budgets for different categories and set savings goals.

### Viewing Dashboard

Load the dashboard to see:
- Total spending
- Spending by category (pie/bar charts)
- Budget status and remaining amounts

### Getting Saving Tips

Click "Get Tips" to receive AI-generated personalized saving suggestions based on your spending patterns and budget goals.

### Importing Sample Data

To test with sample data:
```bash
python -c "
import pandas as pd
from models import Expense, Category
from db import Database
from storage import Storage

db = Database()
storage = Storage(db)
df = pd.read_csv('sample_data.csv')
for _, row in df.iterrows():
    expense = Expense(
        date=row['date'],
        amount=row['amount'],
        currency=row['currency'],
        category=Category(row['category']),
        description=row['description'],
        method=row['method'],
        tags=row['tags'].split(',') if row['tags'] else []
    )
    storage.save_expense(expense)
print('Sample data imported')
"
```

### Running Tests

```bash
python -m pytest tests/
```

## File Structure

- `app.py`: Main Flask application
- `db.py`: SQLite database operations
- `models.py`: Data models (Expense, Budget, UserPrefs)
- `storage.py`: High-level data storage functions
- `processor.py`: Expense processing, categorization, and budget calculations
- `openai_client.py`: OpenAI API integration for tips
- `ui_helpers.py`: Chart generation utilities
- `utils.py`: Helper functions (date parsing, formatting)
- `templates/index.html`: Web interface
- `static/styles.css`: Styling
- `sample_data.csv`: Example expense data
- `tests/test_processor.py`: Unit tests
- `requirements.txt`: Python dependencies

## API Endpoints

- `POST /api/expense`: Add new expense
- `GET /api/dashboard`: Get dashboard data and charts
- `POST /api/budget`: Set/update budget
- `POST /api/tips`: Generate saving tips
- `POST /api/user_prefs`: Update user preferences

## Security & Privacy

- All data stored locally in SQLite database
- No data sent to external servers (except optional OpenAI API calls)
- API key stored in environment variable, never committed to code
- Parameterized SQL queries prevent injection attacks

## Customization

- **Offline Mode**: Comment out OpenAI-related code for fully offline operation
- **Categories**: Modify categorization rules in `processor.py`
- **UI**: Update `templates/index.html` and `static/styles.css`
- **Charts**: Customize visualizations in `ui_helpers.py`

## Development

The application is designed to be modular and extensible. Key areas for enhancement:

- Add expense editing/deletion
- Implement recurring expenses
- Add income tracking
- Create export functionality
- Add more chart types and analytics

## License

This project is open-source and available under the MIT License.

## Disclaimer

This application is for educational and personal use. Always consult with financial professionals for important financial decisions. The AI-generated tips are suggestions based on spending patterns and should not be considered financial advice.
