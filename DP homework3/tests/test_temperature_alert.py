from _pytest.capture import CaptureFixture

from src.observers.temperature_alert import TemperatureAlert


def test_temperature_alert_trigger(capfd: CaptureFixture[str]) -> None:
    alert = TemperatureAlert()
    threshold = alert.threshold  # Get the randomly set threshold

    alert.update(threshold + 1, 50, 5)  # Exceed the threshold
    out, _ = capfd.readouterr()

    assert (f"TemperatureAlert: **Alert! Temperature "
            f"exceeded {threshold}°C → Current: {threshold + 1}°C**") in out


def test_temperature_alert_no_trigger(capfd: CaptureFixture[str]) -> None:
    alert = TemperatureAlert()
    threshold = alert.threshold  # Get the randomly set threshold

    alert.update(threshold - 1, 50, 5)  # Exceed the threshold
    out, _ = capfd.readouterr()

    assert "" == out

