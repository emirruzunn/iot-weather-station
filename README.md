# IoT Weather Station & Sensor Analytics

ESP32 (Wokwi) tabanlı çevresel sensör simülasyonu ve Python CLI veri analiz aracı.

## Desteklenen Metrikler
* **Sıcaklık (°C)** (BME280)
* **Bağıl Nem (%)** (BME280)
* **Hava Basıncı (hPa)** (BME280)
* **Yağış Şiddeti (%)** (Analog Yağış Sensörü)
* **Rüzgar Hızı (km/h)** (Anemometre)

## Kullanım

### 1. Simüle Veri Üretme
```bash
python main.py generate --count 50 --format csv --output data/sim_readings
```
### 2. İstatistiksel Rapor Alma
```bash
# Tüm metrikler
python main.py report --file data/sim_readings.csv

# Belirli bir metrik
python main.py report --file data/sim_readings.csv --metric wind_speed
```