import time
from machine import Pin, ADC

rain_adc = ADC(Pin(34))
rain_adc.atten(ADC.ATTN_11DB)

wind_adc = ADC(Pin(35))
wind_adc.atten(ADC.ATTN_11DB)

print("timestamp,sensor_id,temperature,humidity,pressure,rain_intensity,wind_speed")

while True:
    rain_pct = round((rain_adc.read() / 4095) * 100, 1)
    wind_spd = round((wind_adc.read() / 4095) * 120.0, 1)
    
    # Wokwi BME280 referans simülasyonu
    temp = 24.5
    hum = 55.0
    press = 1013.25
    ts = int(time.time())

    print(f"{ts},WOKWI-ESP32,{temp},{hum},{press},{rain_pct},{wind_spd}")
    time.sleep(2)