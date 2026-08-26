import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from sensors.readers import WokwiWeatherReader, HardwareWeatherReader

# Simülasyon mu gerçek donanım mı? (Wokwi için True, Gerçek ESP32 için False)
SIMULATION_MODE = True

# Ortak OLED Ekran Başlatma (I2C SDA:21, SCL:22)
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
oled = SSD1306_I2C(128, 64, i2c)

# İlgili sürücüyü seç
if SIMULATION_MODE:
    sensor_station = WokwiWeatherReader(dht_pin=15, rain_pin=34, wind_pin=35, hail_pin=32, soil_pin=33)
else:
    sensor_station = HardwareWeatherReader(sda_pin=21, scl_pin=22, rain_pin=34, wind_pin=35, hail_pin=32, soil_pin=33)

while True:
    try:
        temp, hum, press, rain, wind, hail, soil = sensor_station.read()

        # OLED Ekran Güncelleme (7 metrik, 9px aralık)
        oled.fill(0)
        oled.text(f"Sicak:{temp:.1f}C", 0, 0)
        oled.text(f"Nem  :%{hum:.0f}", 0, 9)
        oled.text(f"Bsnc :{press:.0f}hPa", 0, 18)
        oled.text(f"Yagis:%{rain:.0f}", 0, 27)
        oled.text(f"Rzgar:{wind:.1f}km/h", 0, 36)
        oled.text(f"Dolu :%{hail:.0f}", 0, 45)
        oled.text(f"Toprk:%{soil:.0f}", 0, 54)
        oled.show()

    except Exception as err:
        oled.fill(0)
        oled.text("Sensor Hatasi!", 0, 25)
        oled.show()

    time.sleep(1)