import time
from weather_station import WeatherStation
from observers.weather_display import WeatherDisplay
from src.observers.wind_speed_alert import WindSpeedAlert
from src.observers.temperature_alert import TemperatureAlert
from src.observers.humidity_alert import HumidityAlert


def main():
    weather_station = WeatherStation()

    # Initial observer (Weather Display)
    weather_display = WeatherDisplay()
    weather_station.attach(weather_display)

    # Simulate weather updates
    for week in range(1, 21):
        print(f"\n--- Week {week} ---")
        weather_station.simulate_weather_change()

        # Add observers dynamically over time
        if week == 4:
            temp_alert = TemperatureAlert()
            weather_station.attach(temp_alert)
            print("Adding: TemperatureAlert")

        if week == 5:
            wind_alert = WindSpeedAlert()
            weather_station.attach(wind_alert)
            print("Adding: WindSpeedAlert")

        if week == 6:
            humidity_alert = HumidityAlert()
            weather_station.attach(humidity_alert)
            print("Adding: HumidityAlert")

        if week == 8:
            print("Removing: HumidityAlert")
            weather_station.detach(humidity_alert)

        time.sleep(1)  # Pause for readability


if __name__ == "__main__":
    main()
