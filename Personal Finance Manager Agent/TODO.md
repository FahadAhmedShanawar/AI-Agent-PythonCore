# Personal Finance Manager Agent - Development Tasks

## Phase 1: Setup and Core Files
- [x] Create requirements.txt with pinned free dependencies
- [x] Create models.py with dataclasses for Expense, Budget, UserPrefs
- [x] Create db.py with sqlite initialization and CRUD wrappers
- [x] Create storage.py with high-level save/load functions
- [x] Create utils.py with helper utilities (date parsing, currency formatting)

## Phase 2: Processing and AI
- [x] Create processor.py with categorization, aggregation, budget calculations
- [x] Create openai_client.py with OpenAI API wrapper, prompts, retries
- [x] Create ui_helpers.py with chart rendering functions (plotly to PNG/base64)

## Phase 3: UI and Web App
- [x] Create app.py with Flask routes and main app
- [x] Create templates/index.html for single-page UI
- [x] Create static/styles.css for minimal styling

## Phase 4: Data and Testing
- [x] Create sample_data.csv with example expenses
- [x] Create tests/test_processor.py with unit tests
- [x] Create README.md with setup and run instructions

## Phase 5: Integration and Validation
- [x] Install dependencies from requirements.txt
- [x] Run unit tests to verify functionality
- [x] Seed DB with sample data and test dashboard
- [x] Test OpenAI tips generation
- [x] Final demo and validation
