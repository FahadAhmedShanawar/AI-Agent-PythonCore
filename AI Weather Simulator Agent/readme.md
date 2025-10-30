# AI Weather Manipulation Simulator Agent

An AI-powered simulator that predicts and visualizes the potential effects of artificially manipulating weather conditions for specific locations and time periods.

## Features

- **Real-time Weather Data**: Fetches current weather conditions using OpenWeatherMap API
- **Weather Manipulation Simulation**: Simulate effects of rainfall, temperature, humidity, and cloud coverage changes
- **AI-Powered Impact Analysis**: Uses OpenAI to generate detailed impact summaries
- **Interactive Visualizations**: Dynamic charts and heatmaps using Plotly
- **Responsive Web Interface**: Bootstrap 5 based UI with modern design
- **Multiple Scenarios**: Test various climate scenarios (Dubai heat reduction, London rainfall increase, etc.)


# Installation
# Must read to get your agent running
### 1. Create and activate a Python virtual environment (venv)

- macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

- Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

- Windows (Command Prompt):
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Upgrade pip and essential packaging tools
```bash
python -m pip install --upgrade pip setuptools wheel
```

### 3. Install dependencies
- If you already have a requirements.txt:
```bash
pip install -r requirements.txt
```
- If you do not have a requirements.txt, create one with the example packages below, then install:
```text
# Example requirements.txt
Flask>=2.0
requests>=2.25
python-dotenv>=0.19
openai>=0.27
pandas>=1.3
numpy>=1.21
plotly>=5.0
matplotlib>=3.4
meteostat>=1.6      # optional, only if you use Meteostat
gunicorn>=20.0      # optional, for production deployment
```

Save that as `requirements.txt` and run:
```bash
pip install -r requirements.txt
```

### 4. Verify installation
Quick checks:
```bash
pip list
# or
python -c "import flask,requests,openai,pandas; print('OK')"
```

### 5. Environment variables
Create a `.env` file in the project root with keys:
```env
OPENWEATHER_API_KEY=your_openweather_api_key
METEOSTAT_API_KEY=your_meteostat_api_key  # Optional
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key_here
```

### 6. Run and stop
- Run the app:
```bash
python app.py
```
- Stop and deactivate the venv:
```bash
deactivate
```

## API Keys Setup

1. **OpenWeatherMap API**:
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key
   - Add to `.env` as `OPENWEATHER_API_KEY`

2. **OpenAI API**:
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Get your API key
   - Add to `.env` as `OPENAI_API_KEY`

3. **Meteostat API** (Optional):
   - For historical weather data
   - Add to `.env` as `METEOSTAT_API_KEY`

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://localhost:5000`

3. **Configure simulation**:
   - Enter a city name
   - Select manipulation type (rainfall, temperature, humidity, clouds)
   - Adjust intensity (-1 to 1)
   - Set duration (1-30 days)

4. **Run simulation**:
   Click "Run Simulation" to see results

## Project Structure

```
ai-weather-simulator-agent/
├── app.py                      # Flask application main file
├── config.py                   # Configuration and API keys
├── requirements.txt            # Python dependencies
├── readme.md                   # This file
├── data/
│   └── sample_climate.csv      # Sample climate data
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styles
│   └── js/
│       └── script.js          # Frontend JavaScript
├── templates/
│   └── index.html             # Main HTML template
└── utils/
    ├── weather_api.py         # Weather API integrations
    ├── simulation_engine.py   # Weather manipulation logic
    └── visualizer.py          # Chart and visualization generation
```

## API Endpoints

- `GET /` - Main application page
- `POST /api/simulate` - Run weather simulation
- `GET /api/weather-options` - Get available manipulation options
- `GET /api/current-weather/<city>` - Get current weather for a city

## Testing Scenarios

The application includes testing for various scenarios:

1. **Heavy Rain in Dubai**: Simulate increased rainfall in arid climate
2. **Heat Reduction in Karachi**: Test temperature manipulation effects
3. **Cloud Formation in London**: Analyze cloud coverage impacts
4. **Humidity Control**: Study moisture content changes

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs**: OpenWeatherMap, Meteostat, OpenAI
- **Visualization**: Plotly, Matplotlib
- **Data Processing**: Pandas, NumPy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a simulation tool for educational and research purposes. Weather manipulation depicted here is hypothetical and not representative of real-world capabilities or current technology.

---

**Social Media Caption**: "☁️ Explore the science behind climate engineering! My AI Weather Manipulation Simulator Agent predicts and visualizes how modifying rainfall, temperature, or clouds could impact the world. #AI #Weather #Climate #Simulation"
