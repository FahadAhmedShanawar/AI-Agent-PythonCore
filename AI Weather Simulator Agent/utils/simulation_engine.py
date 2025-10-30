import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class WeatherSimulationEngine:
    def __init__(self):
        self.weather_factors = {
            'temperature': {'min': -10, 'max': 50, 'unit': '°C'},
            'humidity': {'min': 0, 'max': 100, 'unit': '%'},
            'rainfall': {'min': 0, 'max': 500, 'unit': 'mm'},
            'wind_speed': {'min': 0, 'max': 50, 'unit': 'm/s'},
            'clouds': {'min': 0, 'max': 100, 'unit': '%'}
        }

    def simulate_weather_manipulation(self, current_weather, manipulation_type, intensity, duration_days=7):
        """
        Simulate the effects of weather manipulation

        Args:
            current_weather: dict with current weather conditions
            manipulation_type: str ('rainfall', 'temperature', 'humidity', 'clouds')
            intensity: float (-1 to 1, negative for decrease, positive for increase)
            duration_days: int number of days to simulate

        Returns:
            dict with simulated weather data and impacts
        """
        simulated_data = []
        impacts = []

        # Base values from current weather
        base_temp = current_weather.get('temperature', 20)
        base_humidity = current_weather.get('humidity', 50)
        base_rainfall = current_weather.get('rainfall', 0)
        base_clouds = current_weather.get('clouds', 20)
        base_wind = current_weather.get('wind_speed', 5)

        for day in range(duration_days):
            # Apply manipulation effects
            if manipulation_type == 'rainfall':
                # Increasing rainfall affects temperature, humidity, clouds
                rainfall_change = intensity * 50 * (1 + day * 0.1)  # Cumulative effect
                temp_change = -intensity * 2 * (rainfall_change / 50)
                humidity_change = intensity * 20
                cloud_change = intensity * 30

            elif manipulation_type == 'temperature':
                # Temperature changes affect humidity and rainfall
                temp_change = intensity * 10
                humidity_change = -intensity * 5
                rainfall_change = intensity * 5 if intensity < 0 else -intensity * 2
                cloud_change = intensity * 10

            elif manipulation_type == 'humidity':
                # Humidity changes affect clouds and rainfall
                humidity_change = intensity * 30
                cloud_change = intensity * 15
                rainfall_change = intensity * 10
                temp_change = -intensity * 1

            elif manipulation_type == 'clouds':
                # Cloud changes affect temperature and rainfall
                cloud_change = intensity * 40
                temp_change = -intensity * 3
                rainfall_change = intensity * 15
                humidity_change = intensity * 10

            else:
                temp_change = humidity_change = rainfall_change = cloud_change = 0

            # Calculate new values with bounds checking
            new_temp = max(self.weather_factors['temperature']['min'],
                          min(self.weather_factors['temperature']['max'],
                              base_temp + temp_change))

            new_humidity = max(self.weather_factors['humidity']['min'],
                              min(self.weather_factors['humidity']['max'],
                                  base_humidity + humidity_change))

            new_rainfall = max(self.weather_factors['rainfall']['min'],
                              base_rainfall + rainfall_change)

            new_clouds = max(self.weather_factors['clouds']['min'],
                            min(self.weather_factors['clouds']['max'],
                                base_clouds + cloud_change))

            # Add some randomness for realism
            new_temp += random.uniform(-1, 1)
            new_humidity += random.uniform(-5, 5)
            new_rainfall = max(0, new_rainfall + random.uniform(-5, 5))
            new_clouds += random.uniform(-10, 10)

            # Ensure bounds after randomness
            new_humidity = max(0, min(100, new_humidity))
            new_clouds = max(0, min(100, new_clouds))

            day_data = {
                'day': day + 1,
                'date': (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d'),
                'temperature': round(new_temp, 1),
                'humidity': round(new_humidity, 1),
                'rainfall': round(new_rainfall, 1),
                'clouds': round(new_clouds, 1),
                'wind_speed': base_wind
            }

            simulated_data.append(day_data)

            # Track impacts
            if day == 0:
                impacts.append(f"Day {day+1}: Initial {manipulation_type} manipulation applied")
            elif day == duration_days - 1:
                impacts.append(f"Day {day+1}: Peak effects observed with cumulative changes")

        return {
            'simulated_weather': simulated_data,
            'manipulation_type': manipulation_type,
            'intensity': intensity,
            'duration_days': duration_days,
            'impacts': impacts,
            'summary': self._generate_simulation_summary(simulated_data, manipulation_type, intensity)
        }

    def _generate_simulation_summary(self, data, manipulation_type, intensity):
        """Generate a summary of the simulation results"""
        if not data:
            return "No simulation data available"

        initial_temp = data[0]['temperature']
        final_temp = data[-1]['temperature']
        total_rainfall = sum(d['rainfall'] for d in data)
        avg_humidity = sum(d['humidity'] for d in data) / len(data)

        direction = "increase" if intensity > 0 else "decrease"

        summary = f"Simulation of {manipulation_type} {direction}: "
        summary += f"Temperature changed from {initial_temp}°C to {final_temp}°C. "
        summary += f"Total rainfall: {total_rainfall:.1f}mm over {len(data)} days. "
        summary += f"Average humidity: {avg_humidity:.1f}%."

        return summary

    def get_manipulation_options(self):
        """Return available manipulation types and their descriptions"""
        return {
            'rainfall': {
                'description': 'Increase or decrease precipitation levels',
                'effects': ['Temperature reduction', 'Humidity increase', 'Cloud formation']
            },
            'temperature': {
                'description': 'Modify ambient temperature',
                'effects': ['Humidity changes', 'Precipitation patterns', 'Cloud coverage']
            },
            'humidity': {
                'description': 'Alter moisture content in air',
                'effects': ['Cloud formation', 'Precipitation likelihood', 'Comfort levels']
            },
            'clouds': {
                'description': 'Control cloud coverage and density',
                'effects': ['Temperature regulation', 'Precipitation control', 'Solar radiation']
            }
        }
