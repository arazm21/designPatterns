class WeatherData:
    """Represents weather data with temperature, humidity, and wind speed."""

    def __init__(self, temperature: float, humidity: float, wind_speed: float) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

    def __str__(self) -> str:
        """String representation of weather data."""
        return f"Temperature: {self.temperature}°C, Humidity: {self.humidity}%, Wind Speed: {self.wind_speed} km/h"
