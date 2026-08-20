import time
import dht
import random
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C

# I2C ve OLED Tanımlaması
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
oled = SSD1306_I2C(128, 64, i2c)

# Sensörler
dht_sensor = dht.DHT22(Pin(15))
rain_adc = ADC(Pin(34))
rain_adc.atten(ADC.ATTN_11DB)
wind_adc = ADC(Pin(35))
wind_adc.atten(ADC.ATTN_11DB)

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        press = round(random.uniform(1010.0, 1015.0), 1)
        
        # Potansiyometre dönüşümleri
        rain_pct = round((rain_adc.read() / 4095) * 100, 0)
        wind_spd = round((wind_adc.read() / 4095) * 120.0, 1)

        # Net Ekran Düzeni
        oled.fill(0)
        oled.text(f"Sicaklik:{temp:.1f} C", 0, 0)
        oled.text(f"Nem     :%{hum:.0f}", 0, 13)
        oled.text(f"Basinc  :{press:.0f} hPa", 0, 26)
        oled.text(f"Yagis   :%{rain_pct:.0f}", 0, 39)
        oled.text(f"Ruzgar  :{wind_spd:.1f}km/h", 0, 52)
        oled.show()

    except Exception as e:
        oled.fill(0)
        oled.text("Sensor Hatasi!", 0, 25)
        oled.show()

    time.sleep(1)