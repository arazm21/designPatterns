import pytest
from src.observers.wind_speed_alert import WindSpeedAlert


def test_wind_speed_alert_trigger(capfd):
    alert = WindSpeedAlert()

    alert.update(25.0, 50, 10)  # First update (no alert)
    alert.update(25.0, 50, 15)  # Wind speed increased

    out, _ = capfd.readouterr()
    assert "💨 WindSpeedAlert: **Alert! Wind speed has increased 1 times in a row!**" in out
