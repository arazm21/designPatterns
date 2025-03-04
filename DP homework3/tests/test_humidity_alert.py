from _pytest.capture import CaptureFixture

from src.observers.humidity_alert import HumidityAlert


def test_humidity_alert_trigger(capfd: CaptureFixture[str]) -> None:
    alert = HumidityAlert()
    threshold = alert.threshold  # Get the randomly set threshold

    alert.update(25.0, threshold + 1, 5)  # Exceed the threshold
    out, _ = capfd.readouterr()

    assert (f"HumidityAlert: **Alert! Humidity "
            f"exceeded {threshold}% → Current: {threshold + 1}%**") in out


def test_humidity_alert_no_trigger(capfd: CaptureFixture[str]) -> None:
    alert = HumidityAlert()
    threshold = alert.threshold  # Get the randomly set threshold

    alert.update(25.0, threshold - 1, 5)  # Exceed the threshold
    out, _ = capfd.readouterr()

    assert "" in out
