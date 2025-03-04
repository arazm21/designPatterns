from _pytest.capture import CaptureFixture

from src.observers.wind_speed_alert import WindSpeedAlert


def test_wind_speed_alert_trigger(capfd: CaptureFixture[str]) -> None:
    alert = WindSpeedAlert()

    alert.update(25.0, 50, 10)  # First update (no alert)
    alert.update(25.0, 50, 15)  # Wind speed increased

    out, _ = capfd.readouterr()
    assert ("WindSpeedAlert: **Alert! Wind speed "
            "has increased 1 time in a row!**") in out


def test_multiple_in_a_row(capfd: CaptureFixture[str]) -> None:
    alert = WindSpeedAlert(amount_of_updates_to_alert=2)

    alert.update(25.0, 50, 10)  # First update (no alert)
    alert.update(25.0, 50, 15)  # Wind speed increased
    alert.update(25.0, 50, 20)  # Wind speed increased
    out, _ = capfd.readouterr()
    assert "2 times" in out

    alert.update(25.0, 50, 25)  # Wind speed increased
    out, _ = capfd.readouterr()
    assert "3 times" in out

    alert.update(25.0, 50, 30)  # Wind speed increased
    out, _ = capfd.readouterr()
    assert "4 times" in out

    alert.update(25.0, 50, 29)  # Wind speed increased
    out, _ = capfd.readouterr()
    assert out == ""
