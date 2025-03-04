from typing import List, Optional

from src.observer import Observer


class WindSpeedAlert(Observer):
    """Triggers an alert if wind speed increases over consecutive updates."""

    def __init__(self, amount_of_updates_to_alert: int = 1) -> None:
        self.previous_wind_speed: Optional[float] = None  # Track the previous speed
        self.amount_of_updates_to_alert: int = amount_of_updates_to_alert
        self.amount_of_increases: int = 0
        self.wind_speed_history: List[float] = []  # Track previous wind speeds

    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if self.previous_wind_speed is not None:
            if wind_speed > self.previous_wind_speed:
                self.amount_of_increases += 1
                self.wind_speed_history.append(self.previous_wind_speed)
                # Store previous wind speed

                if self.amount_of_increases >= self.amount_of_updates_to_alert:
                    history_str = " -> ".join(map(str, self.wind_speed_history
                                                  + [wind_speed]))
                    times_text = "time" if self.amount_of_increases == 1 else "times"
                    print(
                        f"💨 WindSpeedAlert: **Alert! "
                        f"Wind speed has increased "
                        f"{self.amount_of_increases} {times_text} in a "
                        f"row!** ({history_str})"
                    )
            else:
                # Reset if wind speed does not increase
                self.amount_of_increases = 0
                self.wind_speed_history.clear()

        # Store the latest wind speed for the next update
        self.previous_wind_speed = wind_speed
