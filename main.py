import argparse
import csv
import sys

__version__ = "1.3.0"

from sensors.simulator import WeatherSimulator
from storage.logger import save_to_csv, save_to_json
from reporting.stats import calculate_metrics

METRIC_LABELS = {
    "temperature": "Sıcaklık (°C)",
    "humidity": "Nem (%)",
    "pressure": "Basınç (hPa)",
    "rain_intensity": "Yağış Şiddeti (%)",
    "wind_speed": "Rüzgar Hızı (km/h)",
    "hail_intensity": "Dolu Yoğunluğu (darbe/dk)",
    "soil_moisture": "Toprak Nemi (%)"
}

def main():
    parser = argparse.ArgumentParser(description="IoT Meteoroloji İstasyonu Simülatörü ve CLI Analiz Aracı")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate Komutu
    gen_parser = subparsers.add_parser("generate", help="Sanal meteoroloji verisi üretir")
    gen_parser.add_argument("--count", type=int, default=10, help="Üretilecek veri sayısı")
    gen_parser.add_argument("--sensor-id", type=str, default="STATION-01", help="Sensör kimliği")
    gen_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Kayıt formatı")
    gen_parser.add_argument("--output", type=str, default="data/readings", help="Dosya yolu (uzantısız)")

    # Report Komutu
    rep_parser = subparsers.add_parser("report", help="CSV dosyasından metrik raporu üretir")
    rep_parser.add_argument("--file", type=str, required=True, help="Okunacak CSV dosyası yolu")
    rep_parser.add_argument("--metric", choices=list(METRIC_LABELS.keys()), help="Filtrelenecek metrik")

    args = parser.parse_args()

    if args.command == "generate":
        sim = WeatherSimulator(args.sensor_id)
        data = [sim.read_all() for _ in range(args.count)]
        filepath = f"{args.output}.{args.format}"
        
        if args.format == "csv":
            save_to_csv(data, filepath)
        else:
            save_to_json(data, filepath)
        print(f"Başarılı: {args.count} adet veri '{filepath}' dosyasına kaydedildi.")

    elif args.command == "report":
        records = []
        try:
            with open(args.file, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                records = list(reader)
        except FileNotFoundError:
            print(f"Hata: '{args.file}' dosyası bulunamadı.")
            sys.exit(1)

        if not records:
            print(f"Uyarı: '{args.file}' dosyasında veri bulunamadı.")
            sys.exit(0)

        stats = calculate_metrics(records, args.metric)
        print(f"\nMeteoroloji Sensör Raporu — {args.file}")
        print("─" * 60)
        print(f"Toplam Kayıt : {len(records)}")
        print(f"İlk Kayıt    : {records[0].get('timestamp', 'N/A')}")
        print(f"Son Kayıt    : {records[-1].get('timestamp', 'N/A')}\n")

        print(f"{'Metrik':<22} {'Min':<10} {'Max':<10} {'Ortalama':<10}")
        print("─" * 60)
        for m, vals in stats.items():
            isim = METRIC_LABELS.get(m, m)
            print(f"{isim:<22} {vals['min']:<10} {vals['max']:<10} {vals['avg']:<10}")

if __name__ == "__main__":
    main()