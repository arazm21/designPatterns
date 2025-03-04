from _pytest.capture import CaptureFixture

from src.observers.weather_display import WeatherDisplay


def test_weather_display_update(capfd: CaptureFixture[str]) -> None:
    display = WeatherDisplay()
    display.update(25.0, 50, 5)

    out, _ = capfd.readouterr()
    assert ("WeatherDisplay: Temperature = 25.0°C, "
            "Humidity = 50%, Wind Speed = 5 km/h") in out
