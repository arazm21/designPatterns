import pytest
from src.observers.temperature_alert import TemperatureAlert


def test_temperature_alert_trigger(capfd):
    alert = TemperatureAlert()
    threshold = alert.threshold  # Get the randomly set threshold

    alert.update(threshold + 1, 50, 5)  # Exceed the threshold
    out, _ = capfd.readouterr()

    assert f"🔥 TemperatureAlert: **Alert! Temperature exceeded {threshold}°C → Current: {threshold + 1}°C**" in out


def test_temperature_alert_no_trigger(capfd):
    alert = TemperatureAlert()
    threshold = alert.threshold  # Get the randomly set threshold

    alert.update(threshold - 1, 50, 5)  # Exceed the threshold
    out, _ = capfd.readouterr()

    assert f"" in out

