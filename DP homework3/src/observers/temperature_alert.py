import random
from typing import Optional

from src.observer import Observer


class TemperatureAlert(Observer):
    """Triggers an alert if temperature exceeds a random threshold."""

    def __init__(self, threshold: Optional[int] = None) -> None:
        self.threshold: int = threshold if (
                threshold is not None) else random.randint(30, 40)

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if temperature > self.threshold:
            print(f"🔥 TemperatureAlert: **Alert! Temperature "
                  f"exceeded {self.threshold}°C → Current: {temperature}°C**")
