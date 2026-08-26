import time
import random
import dht
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C

# ── Sensör Kurulumu ──────────────────────────────────────
# DHT22 (Sıcaklık & Nem)
dht_sensor = dht.DHT22(Pin(15))

# Potansiyometreler (Analog Sensör Simülasyonları)
rain_adc = ADC(Pin(34))
rain_adc.atten(ADC.ATTN_11DB)

wind_adc = ADC(Pin(35))
wind_adc.atten(ADC.ATTN_11DB)

hail_adc = ADC(Pin(32))
hail_adc.atten(ADC.ATTN_11DB)

soil_adc = ADC(Pin(33))
soil_adc.atten(ADC.ATTN_11DB)

# OLED Ekran (I2C SDA:21, SCL:22)
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
oled = SSD1306_I2C(128, 64, i2c)

# ── Ana Döngü ────────────────────────────────────────────
while True:
    try:
        # DHT22 okuma
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        # Basınç (Wokwi'de simüle)
        press = round(random.uniform(1010.0, 1015.0), 1)

        # Potansiyometre okumaları
        rain = round((rain_adc.read() / 4095) * 100, 1)
        wind = round((wind_adc.read() / 4095) * 120.0, 1)
        hail = round((hail_adc.read() / 4095) * 100, 1)
        soil = round((1 - soil_adc.read() / 4095) * 100, 1)

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