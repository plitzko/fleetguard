"""
Generates static fake data for the PREMA demo.
Creates fleet.csv (current state) and timeseries.csv (last 72h history).
Run once - data is checked into the repo so the demo is reproducible.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

np.random.seed(42)

# Driver names per truck
DRIVERS = [
    "M. Weber", "J. Bauer", "S. Klein", "T. Holm", "A. Graf",
    "P. Roth", "K. Lang", "F. Wolf", "R. Vogel", "H. Stein"
]

# Define current fleet state - LKW-01 is the demo critical case
fleet_state = [
    # id, driver, status, motor_temp, brake_pct, oil_pressure, tire_fl, tire_fr, rul_hours, km_total, load_pct
    ("LKW-01", "M. Weber", "KRITISCH",  98, 12, 2.1, 7.8, 8.1,  48,  287_400, 78),
    ("LKW-02", "J. Bauer", "WARNUNG",   91, 28, 3.2, 8.4, 8.3, 320, 198_650, 65),
    ("LKW-03", "S. Klein", "OK",        76, 84, 4.1, 8.6, 8.5, 1850, 142_300, 45),
    ("LKW-04", "T. Holm",  "OK",        79, 91, 4.0, 8.5, 8.6, 2100,  98_120, 52),
    ("LKW-05", "A. Graf",  "OK",        81, 77, 3.9, 8.4, 8.4, 1620, 215_870, 71),
    ("LKW-06", "P. Roth",  "OK",        78, 82, 4.0, 8.5, 8.5, 1980, 156_440, 38),
    ("LKW-07", "K. Lang",  "WARNUNG",   89, 38, 3.5, 8.2, 8.3, 480, 234_910, 82),
    ("LKW-08", "F. Wolf",  "OK",        77, 88, 4.1, 8.6, 8.5, 2240, 112_580, 41),
    ("LKW-09", "R. Vogel", "OK",        80, 73, 3.8, 8.4, 8.5, 1480, 178_220, 58),
    ("LKW-10", "H. Stein", "OK",        75, 86, 4.0, 8.5, 8.6, 2050, 134_750, 49),
]

cols = ["lkw_id", "driver", "status", "motor_temp_c", "brake_fluid_pct",
        "oil_pressure_bar", "tire_fl_bar", "tire_fr_bar", "rul_hours",
        "km_total", "load_pct"]

fleet_df = pd.DataFrame(fleet_state, columns=cols)
fleet_df.to_csv(DATA_DIR / "fleet.csv", index=False)
print(f"fleet.csv: {len(fleet_df)} trucks")

# Generate 72h timeseries for each truck (1 measurement per hour)
end_time = datetime(2026, 5, 5, 14, 0, 0)
hours = 72
timeseries = []

for _, truck in fleet_df.iterrows():
    for h in range(hours):
        ts = end_time - timedelta(hours=hours - h - 1)

        # LKW-01: degrading brake fluid from 80% to 12%
        if truck["lkw_id"] == "LKW-01":
            progress = h / (hours - 1)
            # Smooth degradation curve, slightly accelerating
            brake = 80 - (80 - 12) * (progress ** 1.4)
            motor_t = 82 + (98 - 82) * progress + np.random.normal(0, 0.8)
            oil_p = 4.0 - (4.0 - 2.1) * progress + np.random.normal(0, 0.05)
        # LKW-02: warning level brake degradation
        elif truck["lkw_id"] == "LKW-02":
            progress = h / (hours - 1)
            brake = 65 - (65 - 28) * progress
            motor_t = truck["motor_temp_c"] + np.random.normal(0, 1.2)
            oil_p = truck["oil_pressure_bar"] + np.random.normal(0, 0.08)
        # LKW-07: warning level
        elif truck["lkw_id"] == "LKW-07":
            progress = h / (hours - 1)
            brake = 70 - (70 - 38) * progress
            motor_t = truck["motor_temp_c"] + np.random.normal(0, 1.2)
            oil_p = truck["oil_pressure_bar"] + np.random.normal(0, 0.08)
        # All others: stable with normal noise
        else:
            brake = truck["brake_fluid_pct"] + np.random.normal(0, 0.5)
            motor_t = truck["motor_temp_c"] + np.random.normal(0, 1.5)
            oil_p = truck["oil_pressure_bar"] + np.random.normal(0, 0.1)

        timeseries.append({
            "lkw_id": truck["lkw_id"],
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "brake_fluid_pct": round(max(0, brake), 1),
            "motor_temp_c": round(motor_t, 1),
            "oil_pressure_bar": round(oil_p, 2),
        })

ts_df = pd.DataFrame(timeseries)
ts_df.to_csv(DATA_DIR / "timeseries.csv", index=False)
print(f"timeseries.csv: {len(ts_df)} datapoints ({len(fleet_df)} trucks x {hours}h)")

# Generate alert feed
alerts = [
    ("2026-05-05 08:12", "KRITISCH", "LKW-01", "Bremse 12 % – sofortige Wartung", "XGBoost-Klassifikation", 600),
    ("2026-05-05 07:55", "WARNUNG",  "LKW-02", "Motortemp. 91 °C – prüfen",       "XGBoost-Klassifikation", 600),
    ("2026-05-04 19:30", "INFO",     "LKW-05", "Anomalie erkannt (ISO-Forest)",   "Isolation Forest",        600),
    ("2026-05-04 14:30", "WARNUNG",  "LKW-02", "Bremse 28 % – Wartung einplanen", "XGBoost-Klassifikation", 600),
    ("2026-05-04 09:00", "INFO",     "LKW-03", "Anomalie erkannt (ISO-Forest)",   "Isolation Forest",        600),
    ("2026-05-03 16:20", "INFO",     "LKW-07", "Öldruck leicht erhöht",           "XGBoost-Klassifikation", 600),
    ("2026-05-03 11:15", "WARNUNG",  "LKW-07", "Bremse 42 % – Wartung einplanen", "XGBoost-Klassifikation", 600),
    ("2026-05-02 22:08", "INFO",     "LKW-09", "Reifendruck-Schwankung erkannt",  "Isolation Forest",        600),
    ("2026-05-02 14:45", "INFO",     "LKW-01", "Anomalie erkannt (ISO-Forest)",   "Isolation Forest",        600),
    ("2026-05-01 09:30", "INFO",     "LKW-05", "Öltemperatur grenzwertig",        "XGBoost-Klassifikation", 600),
]

alerts_df = pd.DataFrame(alerts, columns=["timestamp", "severity", "lkw_id", "message", "source", "savings_eur"])
alerts_df.to_csv(DATA_DIR / "alerts.csv", index=False)
print(f"alerts.csv: {len(alerts_df)} alerts")

# Per-truck alert history (for detail view)
truck_alerts = [
    ("LKW-01", "2026-05-05 08:12", "KRITISCH", "Bremse unter 15 % – Sofortmaßnahme"),
    ("LKW-01", "2026-05-04 14:30", "WARNUNG", "Bremse unter 30 % – Wartung einplanen"),
    ("LKW-01", "2026-05-02 14:45", "INFO", "Anomalie erkannt (Isolation Forest)"),
    ("LKW-02", "2026-05-05 07:55", "WARNUNG", "Motortemp. 91 °C – prüfen"),
    ("LKW-02", "2026-05-04 14:30", "WARNUNG", "Bremse 28 % – Wartung einplanen"),
    ("LKW-07", "2026-05-03 16:20", "INFO", "Öldruck leicht erhöht"),
    ("LKW-07", "2026-05-03 11:15", "WARNUNG", "Bremse 42 % – Wartung einplanen"),
]
ta_df = pd.DataFrame(truck_alerts, columns=["lkw_id", "timestamp", "severity", "message"])
ta_df.to_csv(DATA_DIR / "truck_alerts.csv", index=False)
print(f"truck_alerts.csv: {len(ta_df)} truck-specific alerts")
