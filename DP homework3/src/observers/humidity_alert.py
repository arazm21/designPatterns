import random
from src.observer import Observer


class HumidityAlert(Observer):
    """Triggers an alert if humidity exceeds a random threshold."""

    def __init__(self, threshold=random.randint(70, 90)) -> None:
        self.threshold = threshold  # Generate a random threshold

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if humidity > self.threshold:
            print(f"💧 HumidityAlert: **Alert! Humidity exceeded {self.threshold}% → Current: {humidity}%**")
