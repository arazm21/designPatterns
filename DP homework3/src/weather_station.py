import random
from typing import List
from src.observer import Observer, Subject
from src.weather_data import WeatherData


class WeatherStation(Subject):
    """The WeatherStation is the subject that stores and updates weather data, notifying observers when changes occur."""

    def __init__(self) -> None:
        super().__init__()
        self._weather_data = WeatherData(temperature=25.0, humidity=50.0, wind_speed=10.0)

    def attach(self, observer: Observer) -> None:
        """Registers an observer."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Unregisters an observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        """Notifies all observers about updated weather data."""
        for observer in self._observers:
            observer.update(self._weather_data.temperature, self._weather_data.humidity, self._weather_data.wind_speed)

    def set_weather_data(self, temperature: float, humidity: float, wind_speed: float) -> None:
        """Updates weather data and notifies observers."""
        self._weather_data = WeatherData(temperature, humidity, wind_speed)
        self.notify()

    def simulate_weather_change(self) -> None:
        """Simulates weather changes with random values."""
        new_temperature = round(random.uniform(20, 45), 1)
        new_humidity = round(random.uniform(30, 95), 1)
        new_wind_speed = round(random.uniform(5, 40), 1)

        print(f"\nUpdating weather data: {new_temperature}°C, {new_humidity}%, {new_wind_speed} km/h")
        self.set_weather_data(new_temperature, new_humidity, new_wind_speed)
