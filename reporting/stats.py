def calculate_metrics(records, target_metric=None):
    metrics = ["temperature", "humidity", "pressure", "rain_intensity", "wind_speed", "hail_intensity", "soil_moisture"]
    if target_metric:
        metrics = [target_metric]

    stats = {}
    for m in metrics:
        values = []
        for r in records:
            if m in r and r[m] not in ("", None):
                try:
                    values.append(float(r[m]))
                except ValueError:
                    continue
        if values:
            stats[m] = {
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "avg": round(sum(values) / len(values), 2)
            }
    return stats