from _pytest.capture import CaptureFixture

from src.observers.weather_display import WeatherDisplay
from src.weather_station import WeatherStation


def test_register_observer() -> None:
    station = WeatherStation()
    display = WeatherDisplay()

    station.attach(display)
    assert len(station._observers) == 1


def test_register_observers() -> None:
    station = WeatherStation()
    display = WeatherDisplay()
    display2 = WeatherDisplay()

    station.attach(display)
    station.attach(display2)

    assert len(station._observers) == 2


def test_remove_observer_twice() -> None:
    station = WeatherStation()
    display = WeatherDisplay()
    display2 = WeatherDisplay()

    station.attach(display)
    station.attach(display2)
    station.detach(display2)
    station.detach(display2)

    assert len(station._observers) == 1


def test_remove_observer() -> None:
    station = WeatherStation()
    display = WeatherDisplay()

    station.attach(display)
    station.detach(display)
    assert len(station._observers) == 0


def test_notify_observers(capfd: CaptureFixture[str]) -> None:
    station = WeatherStation()
    display = WeatherDisplay()

    station.attach(display)
    station.set_weather_data(30.5, 60, 10)

    out, _ = capfd.readouterr()  # Capture printed output
    assert ("WeatherDisplay: Temperature = 30.5°C, "
            "Humidity = 60%, Wind Speed = 10 km/h") in out
