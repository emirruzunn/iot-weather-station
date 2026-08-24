import time
import random
from machine import Pin, I2C, ADC

class WokwiWeatherReader:
    """Wokwi ortamı için DHT22 + Potansiyometre + Simüle Basınç sürücüsü"""
    def __init__(self, dht_pin=15, rain_pin=34, wind_pin=35):
        import dht
        self.dht = dht.DHT22(Pin(dht_pin))
        self.rain_adc = ADC(Pin(rain_pin))
        self.rain_adc.atten(ADC.ATTN_11DB)
        self.wind_adc = ADC(Pin(wind_pin))
        self.wind_adc.atten(ADC.ATTN_11DB)

    def read(self):
        self.dht.measure()
        temp = self.dht.temperature()
        hum = self.dht.humidity()
        press = round(random.uniform(1010.0, 1015.0), 1)
        rain = round((self.rain_adc.read() / 4095) * 100, 1)
        wind = round((self.wind_adc.read() / 4095) * 120.0, 1)
        return temp, hum, press, rain, wind


class HardwareWeatherReader:
    """Gerçek ESP32 için BME280 (I2C) + Analog Yağış/Rüzgar/Dolu/Toprak Nemi Sensörleri"""
    def __init__(self, sda_pin=21, scl_pin=22, rain_pin=34, wind_pin=35, hail_pin=32, soil_pin=33):
        import bme280
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=100000)
        self.bme = bme280.BME280(i2c=self.i2c)
        self.rain_adc = ADC(Pin(rain_pin))
        self.rain_adc.atten(ADC.ATTN_11DB)
        self.wind_adc = ADC(Pin(wind_pin))
        self.wind_adc.atten(ADC.ATTN_11DB)
        self.hail_adc = ADC(Pin(hail_pin))
        self.hail_adc.atten(ADC.ATTN_11DB)
        self.soil_adc = ADC(Pin(soil_pin))
        self.soil_adc.atten(ADC.ATTN_11DB)

    def read(self):
        # BME280 gerilim/veri okuması
        t_str, p_str, h_str = self.bme.values
        temp = float(t_str.replace("C", ""))
        press = float(p_str.replace("hPa", ""))
        hum = float(h_str.replace("%", ""))
        
        rain = round((self.rain_adc.read() / 4095) * 100, 1)
        wind = round((self.wind_adc.read() / 4095) * 120.0, 1)
        hail = round((self.hail_adc.read() / 4095) * 100, 1)
        soil = round((1 - self.soil_adc.read() / 4095) * 100, 1)  # Kapasitif: düşük değer = yüksek nem
        return temp, hum, press, rain, wind, hail, soil