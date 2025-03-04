import random
from typing import Optional

from src.observer import Observer


class HumidityAlert(Observer):
    """Triggers an alert if humidity exceeds a random threshold."""

    def __init__(self, threshold: Optional[int] = None) -> None:
        self.threshold: int = threshold if (
                threshold is not None) else random.randint(70, 90)

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if humidity > self.threshold:
            print(f"💧 HumidityAlert: **Alert! Humidity "
                  f"exceeded {self.threshold}% → Current: {humidity}%**")
