from flask import Flask, render_template, request, jsonify
import openai
from utils.weather_api import WeatherAPI
from utils.simulation_engine import WeatherSimulationEngine
from utils.visualizer import WeatherVisualizer
from config import OPENAI_API_KEY, DEBUG
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize components
weather_api = WeatherAPI()
simulation_engine = WeatherSimulationEngine()
visualizer = WeatherVisualizer()

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/simulate', methods=['POST'])
def simulate_weather():
    """API endpoint for weather simulation"""
    try:
        data = request.get_json()

        city = data.get('city', 'London')
        manipulation_type = data.get('manipulation_type', 'rainfall')
        intensity = float(data.get('intensity', 0.5))
        duration = int(data.get('duration', 7))

        # Get current weather
        current_weather = weather_api.get_current_weather(city)
        if not current_weather:
            return jsonify({'error': 'Unable to fetch current weather data'}), 400

        # Run simulation
        simulation_results = simulation_engine.simulate_weather_manipulation(
            current_weather, manipulation_type, intensity, duration
        )

        # Generate visualizations
        charts_html = visualizer.create_comparison_charts(
            current_weather, simulation_results['simulated_weather'], manipulation_type
        )

        heatmap_html = visualizer.create_impact_heatmap(simulation_results['simulated_weather'])

        # Generate AI impact summary
        ai_summary = generate_ai_impact_summary(
            current_weather, simulation_results, manipulation_type, city
        )

        # Generate weather report
        report_html = visualizer.generate_weather_report(current_weather, simulation_results)

        return jsonify({
            'success': True,
            'current_weather': current_weather,
            'simulation_results': simulation_results,
            'charts_html': charts_html,
            'heatmap_html': heatmap_html,
            'ai_summary': ai_summary,
            'report_html': report_html
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather-options', methods=['GET'])
def get_weather_options():
    """Get available manipulation options"""
    options = simulation_engine.get_manipulation_options()
    return jsonify(options)

@app.route('/api/current-weather/<city>', methods=['GET'])
def get_current_weather(city):
    """Get current weather for a city"""
    weather_data = weather_api.get_current_weather(city)
    if weather_data:
        return jsonify(weather_data)
    return jsonify({'error': 'Unable to fetch weather data'}), 400

def generate_ai_impact_summary(current_weather, simulation_results, manipulation_type, city):
    """Generate AI-powered impact summary using OpenAI"""
    try:
        if not OPENAI_API_KEY:
            return "AI summary unavailable - OpenAI API key not configured"

        prompt = f"""
        Analyze the potential environmental and societal impacts of artificially manipulating {manipulation_type} in {city}.

        Current weather conditions:
        - Temperature: {current_weather['temperature']}°C
        - Humidity: {current_weather['humidity']}%
        - Rainfall: {current_weather['rainfall']}mm
        - Cloud coverage: {current_weather['clouds']}%

        Simulation results: {simulation_results['summary']}

        Provide a concise but informative summary (2-3 paragraphs) of the potential impacts, including:
        1. Environmental effects
        2. Societal implications
        3. Potential risks or benefits
        4. Long-term considerations

        Keep the tone informative and neutral, focusing on scientific and practical aspects.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI summary generation failed: {str(e)}"

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
