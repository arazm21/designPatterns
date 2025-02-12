from src.observer import Observer


class WeatherDisplay(Observer):
    """Displays the current weather data."""

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        print(f"WeatherDisplay: Temperature = {temperature}°C, Humidity = {humidity}%, Wind Speed = {wind_speed} km/h")
