from src.observer import Observer


class WindSpeedAlert(Observer):
    """Triggers an alert if wind speed increases over consecutive updates."""

    def __init__(self, amount_of_updates_to_alert=1) -> None:
        self.previous_wind_speed = None  # Track the previous wind speed
        self.amount_of_updates_to_alert = amount_of_updates_to_alert
        self.amount_of_increases = 0
    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        if self.previous_wind_speed is not None:
            if wind_speed > self.previous_wind_speed:
                self.amount_of_increases += 1
            else:
                self.amount_of_increases = 0  # Reset if wind speed doesn't increase

            if self.amount_of_increases >= self.amount_of_updates_to_alert:
                print(
                    f"💨 WindSpeedAlert: **Alert! Wind speed has increased {self.amount_of_updates_to_alert} times in a row!**"
                )
                self.amount_of_increases = 0  # Reset after triggering alert

        self.previous_wind_speed = wind_speed  # Store the latest wind speed