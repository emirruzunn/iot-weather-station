import random
import time

class WeatherSimulator:
    def __init__(self, sensor_id="SIM-STATION-01"):
        self.sensor_id = sensor_id

    def read_all(self):
        return {
            "timestamp": int(time.time()),
            "sensor_id": self.sensor_id,
            "temperature": round(random.uniform(15.0, 32.0), 2),     # °C
            "humidity": round(random.uniform(30.0, 85.0), 2),        # %
            "pressure": round(random.uniform(990.0, 1025.0), 2),     # hPa
            "rain_intensity": round(random.uniform(0.0, 100.0), 1),  # %
            "wind_speed": round(random.uniform(0.0, 90.0), 1),       # km/h
            "hail_intensity": round(random.uniform(0.0, 100.0), 1),  # darbe/dk
            "soil_moisture": round(random.uniform(0.0, 100.0), 1)    # %
        }