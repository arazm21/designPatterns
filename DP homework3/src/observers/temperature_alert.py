import random
from src.observer import Observer


class TemperatureAlert(Observer):
    """Triggers an alert if temperature exceeds a random threshold."""

    def __init__(self, threshold=random.randint(30, 35)) -> None:
        self.threshold = threshold  # Generate a random threshold

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if temperature > self.threshold:
            print(f"🔥 TemperatureAlert: **Alert! Temperature exceeded {self.threshold}°C → Current: {temperature}°C**")
