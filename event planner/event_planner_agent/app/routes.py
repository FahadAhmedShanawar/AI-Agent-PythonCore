from flask import request, jsonify, render_template, redirect, url_for
import pandas as pd
import os
from datetime import datetime
from services.venue_finder import VenueFinder
from services.rsvp_manager import RSVPManager
from services.todo_generator import TodoGenerator
from utils.geocode import GeocodeUtil

# Initialize services
venue_finder = VenueFinder()
rsvp_manager = RSVPManager()
todo_generator = TodoGenerator()
geocode_util = GeocodeUtil()

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/events', methods=['GET', 'POST'])
    def events():
        if request.method == 'POST':
            # Create new event
            event_data = request.form.to_dict()
            # Validate and normalize inputs
            event_data['date'] = datetime.fromisoformat(event_data['date']).date().isoformat()
            # Save to CSV
            events_df = pd.read_csv('data/events.csv') if os.path.exists('data/events.csv') else pd.DataFrame()
            events_df = pd.concat([events_df, pd.DataFrame([event_data])], ignore_index=True)
            events_df.to_csv('data/events.csv', index=False)
            return redirect(url_for('events'))
        # List events
        events_df = pd.read_csv('data/events.csv') if os.path.exists('data/events.csv') else pd.DataFrame()
        return render_template('events.html', events=events_df.to_dict('records'))

    @app.route('/venues/<event_id>')
    def venues(event_id):
        # Get event details
        events_df = pd.read_csv('data/events.csv')
        event = events_df[events_df['id'] == int(event_id)].iloc[0]
        # Find venues
        venues = venue_finder.find_venues(event['location'], event['budget'], event['expected_attendees'])
        return render_template('venues.html', event=event, venues=venues)

    @app.route('/rsvps/<event_id>', methods=['GET', 'POST'])
    def rsvps(event_id):
        if request.method == 'POST':
            rsvp_data = request.form.to_dict()
            rsvp_manager.add_rsvp(event_id, rsvp_data)
            return redirect(url_for('rsvps', event_id=event_id))
        # List RSVPs
        rsvps = rsvp_manager.get_rsvps(event_id)
        return render_template('rsvps.html', event_id=event_id, rsvps=rsvps)

    @app.route('/todos/<event_id>')
    def todos(event_id):
        # Get event details
        events_df = pd.read_csv('data/events.csv')
        event = events_df[events_df['id'] == int(event_id)].iloc[0]
        # Generate todos
        todos = todo_generator.generate_todos(event)
        return render_template('todos.html', event=event, todos=todos)

    # API endpoints for AJAX
    @app.route('/api/events', methods=['POST'])
    def api_create_event():
        data = request.get_json()
        # Validate inputs
        required_fields = ['name', 'date', 'time', 'location', 'expected_attendees', 'event_type', 'budget']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        # Normalize date/time
        data['date'] = datetime.fromisoformat(data['date']).date().isoformat()
        # Save
        events_df = pd.read_csv('data/events.csv') if os.path.exists('data/events.csv') else pd.DataFrame()
        data['id'] = len(events_df) + 1
        events_df = pd.concat([events_df, pd.DataFrame([data])], ignore_index=True)
        events_df.to_csv('data/events.csv', index=False)
        return jsonify({'message': 'Event created', 'id': data['id']})

    @app.route('/api/venues')
    def api_venues():
        location = request.args.get('location')
        budget = float(request.args.get('budget', 0))
        attendees = int(request.args.get('attendees', 0))
        venues = venue_finder.find_venues(location, budget, attendees)
        return jsonify(venues)

    @app.route('/api/rsvps/<event_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def api_rsvps(event_id):
        if request.method == 'GET':
            rsvps = rsvp_manager.get_rsvps(event_id)
            return jsonify(rsvps)
        elif request.method == 'POST':
            data = request.get_json()
            rsvp_manager.add_rsvp(event_id, data)
            return jsonify({'message': 'RSVP added'})
        elif request.method == 'PUT':
            data = request.get_json()
            rsvp_manager.update_rsvp(event_id, data['attendee_id'], data)
            return jsonify({'message': 'RSVP updated'})
        elif request.method == 'DELETE':
            attendee_id = request.args.get('attendee_id')
            rsvp_manager.delete_rsvp(event_id, attendee_id)
            return jsonify({'message': 'RSVP deleted'})

    @app.route('/api/todos/<event_id>')
    def api_todos(event_id):
        events_df = pd.read_csv('data/events.csv')
        event = events_df[events_df['id'] == int(event_id)].iloc[0].to_dict()
        todos = todo_generator.generate_todos(event)
        return jsonify(todos)

    @app.route('/export/todos/<event_id>/<format>')
    def export_todos(event_id, format):
        events_df = pd.read_csv('data/events.csv')
        event = events_df[events_df['id'] == int(event_id)].iloc[0].to_dict()
        todos = todo_generator.generate_todos(event)
        if format == 'csv':
            df = pd.DataFrame(todos)
            return df.to_csv(index=False)
        elif format == 'json':
            return jsonify(todos)
        elif format == 'pdf':
            # Generate PDF (simplified)
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 750, f"To-Do List for {event['name']}")
            y = 700
            for todo in todos:
                p.drawString(100, y, f"- {todo['task']} (Due: {todo['deadline']})")
                y -= 20
            p.save()
            buffer.seek(0)
            return buffer.read(), 200, {'Content-Type': 'application/pdf'}
