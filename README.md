# 🌦️ IoT Weather Station & Sensor Analytics

ESP32 tabanlı meteoroloji istasyonu (Wokwi simülasyonu ve gerçek donanım desteği) ile toplanan çevresel verileri toplayan, saklayan ve analiz eden Python CLI aracı.

---

## 📌 Desteklenen Metrikler & Donanım Yapısı

| Metrik | Wokwi Simülasyonu | Gerçek Donanım | Birim | ESP32 Pini |
| :--- | :--- | :--- | :--- | :--- |
| **Sıcaklık** | DHT22 | BME280 | °C | GPIO 15 (DHT) / GPIO 21-22 (I2C) |
| **Nem** | DHT22 | BME280 | % | GPIO 15 (DHT) / GPIO 21-22 (I2C) |
| **Basınç** | Simüle (1010-1015) | BME280 | hPa | - / GPIO 21-22 (I2C) |
| **Yağış Şiddeti** | Potansiyometre | Analog Yağış Sensörü | % | GPIO 34 (ADC1) |
| **Rüzgar Hızı** | Potansiyometre | Analog Anemometre | km/h | GPIO 35 (ADC1) |
| **Görsel Ekran** | SSD1306 OLED (128x64) | SSD1306 OLED (128x64) | - | SDA: 21, SCL: 22 (I2C) |

---

## 🛠️ Kurulum

### 1. Repoyu Klonlayın
```bash
git clone [https://github.com/](https://github.com/)<kullanici-adiniz>/iot-weather-station.git
cd iot-weather-station
```

### 2. Sanal Ortamı Başlatın ve Gereksinimleri Yükleyin
```bash
# Sanal ortam oluşturma (Opsiyonel)
python -m venv venv

# Sanal ortamı aktif etme (Windows):
venv\Scripts\activate
# Sanal ortamı aktif etme (Linux / macOS):
# source venv/bin/activate

# Paketleri yükleme
pip install -r requirements.txt
```

---

## 🚀 Çalıştırma Kılavuzu

### 1. Wokwi Simülasyonu (MicroPython / ESP32)
1. [Wokwi](https://wokwi.com) üzerinde bir **ESP32 MicroPython** projesi açın.
2. `wokwi/diagram.json` dosyasını Wokwi'deki `diagram.json` sekmesine yapıştırın.
3. `wokwi/ssd1306.py` dosyasını yeni sekme açarak yükleyin.
4. `wokwi/main.py` dosyasını ana kod editörüne yapıştırın.
5. Yeşil **Play** butonuna basarak simülasyonu başlatın. Veriler doğrudan OLED ekranda güncellenecektir.

---

### 2. Bilgisayar CLI Aracı (Veri Üretme & Analiz)

#### A. Sanal Veri Üretme (`generate`)
Donanım olmadan test yapmak için sanal meteoroloji verisi üretir:
```bash
# Varsayılan (10 adet CSV verisi üretir -> data/readings.csv)
python main.py generate

# 100 adet özelleştirilmiş CSV verisi üretme
python main.py generate --count 100 --sensor-id STATION-01 --format csv --output data/readings

# JSON formatında veri üretme
python main.py generate --count 50 --format json --output data/readings
```

#### B. İstatistiksel Rapor Alma (`report`)
Kaydedilen CSV dosyası üzerinden Min, Max ve Ortalama değerleri analiz eder:
```bash
# Tüm metriklerin genel istatistik raporu
python main.py report --file data/readings.csv

# Sadece belirli bir metriği filtreleme
python main.py report --file data/readings.csv --metric wind_speed
python main.py report --file data/readings.csv --metric temperature
python main.py report --file data/readings.csv --metric rain_intensity
```

---

## 📂 Proje Dizin Yapısı

```text
iot-weather-station/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py                  # PC tarafındaki CLI aracı (generate & report)
├── sensors/
│   ├── __init__.py
│   ├── simulator.py         # 5 metrikli sahte veri üreticisi
│   └── readers.py           # Donanım & simülasyon sensör okuyucuları
├── storage/
│   ├── __init__.py
│   └── logger.py            # CSV / JSON kayıt modülü
├── reporting/
│   ├── __init__.py
│   └── stats.py             # İstatistik hesaplama modülü
├── data/
│   └── .gitkeep
└── wokwi/
    ├── diagram.json         # Devre şeması (ESP32 + DHT22 + OLED + Potansiyometreler)
    ├── ssd1306.py           # OLED ekran sürücüsü
    └── main.py              # ESP32 üzerinde çalışan MicroPython kodu
```

---

## 🧪 Testleri Çalıştırma

```bash
pytest
```