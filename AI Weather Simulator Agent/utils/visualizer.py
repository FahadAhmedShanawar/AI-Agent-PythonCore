import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from datetime import datetime

class WeatherVisualizer:
    def __init__(self):
        self.colors = {
            'temperature': '#FF6B6B',
            'humidity': '#4ECDC4',
            'rainfall': '#45B7D1',
            'clouds': '#96CEB4',
            'current': '#FFA07A',
            'simulated': '#98D8C8'
        }

    def create_comparison_charts(self, current_weather, simulated_data, manipulation_type):
        """
        Create comparison charts between current and simulated weather
        Returns HTML div with embedded Plotly charts
        """
        # Prepare data
        dates = [d['date'] for d in simulated_data]
        temps = [d['temperature'] for d in simulated_data]
        humidities = [d['humidity'] for d in simulated_data]
        rainfalls = [d['rainfall'] for d in simulated_data]
        clouds = [d['clouds'] for d in simulated_data]

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)', 'Cloud Coverage (%)'),
            specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                   [{'type': 'bar'}, {'type': 'scatter'}]]
        )

        # Temperature
        fig.add_trace(
            go.Scatter(x=dates, y=[current_weather['temperature']] * len(dates),
                      name='Current', line=dict(color=self.colors['current'], dash='dash')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=dates, y=temps, name='Simulated',
                      line=dict(color=self.colors['temperature'])),
            row=1, col=1
        )

        # Humidity
        fig.add_trace(
            go.Scatter(x=dates, y=[current_weather['humidity']] * len(dates),
                      name='Current', line=dict(color=self.colors['current'], dash='dash'), showlegend=False),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=dates, y=humidities, name='Simulated',
                      line=dict(color=self.colors['humidity']), showlegend=False),
            row=1, col=2
        )

        # Rainfall
        fig.add_trace(
            go.Bar(x=dates, y=rainfalls, name='Simulated Rainfall',
                  marker_color=self.colors['rainfall']),
            row=2, col=1
        )

        # Clouds
        fig.add_trace(
            go.Scatter(x=dates, y=[current_weather['clouds']] * len(dates),
                      name='Current', line=dict(color=self.colors['current'], dash='dash'), showlegend=False),
            row=2, col=2
        )
        fig.add_trace(
            go.Scatter(x=dates, y=clouds, name='Simulated',
                      line=dict(color=self.colors['clouds']), showlegend=False),
            row=2, col=2
        )

        # Update layout
        fig.update_layout(
            height=600,
            title_text=f"Weather Manipulation Simulation: {manipulation_type.title()}",
            showlegend=True
        )

        # Update axes
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=2)

        return fig.to_html(full_html=False, include_plotlyjs='cdn')

    def create_impact_heatmap(self, simulated_data):
        """Create a heatmap showing weather parameter correlations"""
        import numpy as np

        # Extract data
        temps = [d['temperature'] for d in simulated_data]
        humidities = [d['humidity'] for d in simulated_data]
        rainfalls = [d['rainfall'] for d in simulated_data]
        clouds = [d['clouds'] for d in simulated_data]

        # Create correlation matrix
        data = np.array([temps, humidities, rainfalls, clouds])
        corr_matrix = np.corrcoef(data)

        labels = ['Temperature', 'Humidity', 'Rainfall', 'Clouds']

        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=labels,
            y=labels,
            colorscale='RdBu',
            zmin=-1, zmax=1
        ))

        fig.update_layout(
            title="Weather Parameter Correlations",
            height=400
        )

        return fig.to_html(full_html=False, include_plotlyjs='cdn')

    def create_matplotlib_charts(self, current_weather, simulated_data, manipulation_type):
        """Create matplotlib charts and return as base64 encoded images"""
        charts = {}

        # Temperature comparison
        plt.figure(figsize=(10, 6))
        dates = [d['date'] for d in simulated_data]
        temps = [d['temperature'] for d in simulated_data]

        plt.plot(dates, [current_weather['temperature']] * len(dates),
                label='Current', linestyle='--', color=self.colors['current'])
        plt.plot(dates, temps, label='Simulated', color=self.colors['temperature'])
        plt.title(f'Temperature Changes - {manipulation_type.title()} Manipulation')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        charts['temperature'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        # Rainfall bar chart
        plt.figure(figsize=(10, 6))
        rainfalls = [d['rainfall'] for d in simulated_data]
        plt.bar(dates, rainfalls, color=self.colors['rainfall'])
        plt.title('Simulated Rainfall')
        plt.xlabel('Date')
        plt.ylabel('Rainfall (mm)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        charts['rainfall'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        return charts

    def generate_weather_report(self, current_weather, simulation_results):
        """Generate a textual weather report"""
        report = f"""
        <div class="weather-report">
            <h4>Weather Manipulation Report</h4>
            <p><strong>Current Conditions:</strong></p>
            <ul>
                <li>Temperature: {current_weather['temperature']}°C</li>
                <li>Humidity: {current_weather['humidity']}%</li>
                <li>Rainfall: {current_weather['rainfall']}mm</li>
                <li>Cloud Coverage: {current_weather['clouds']}%</li>
                <li>Description: {current_weather['description']}</li>
            </ul>

            <p><strong>Simulation Summary:</strong></p>
            <p>{simulation_results['summary']}</p>

            <p><strong>Key Impacts:</strong></p>
            <ul>
        """

        for impact in simulation_results['impacts'][:3]:  # Show first 3 impacts
            report += f"<li>{impact}</li>"

        report += """
            </ul>
        </div>
        """

        return report
