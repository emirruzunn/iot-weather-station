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
    sensor_station = WokwiWeatherReader(dht_pin=15, rain_pin=34, wind_pin=35)
else:
    sensor_station = HardwareWeatherReader(sda_pin=21, scl_pin=22, rain_pin=34, wind_pin=35)

while True:
    try:
        temp, hum, press, rain, wind = sensor_station.read()

        # OLED Ekran Güncelleme
        oled.fill(0)
        oled.text(f"Sicaklik:{temp:.1f} C", 0, 0)
        oled.text(f"Nem     :%{hum:.0f}", 0, 13)
        oled.text(f"Basinc  :{press:.0f} hPa", 0, 26)
        oled.text(f"Yagis   :%{rain:.0f}", 0, 39)
        oled.text(f"Ruzgar  :{wind:.1f}km/h", 0, 52)
        oled.show()

    except Exception as err:
        oled.fill(0)
        oled.text("Sensor Hatasi!", 0, 25)
        oled.show()

    time.sleep(1)